#!/usr/bin/env python3
# pyright: reportMissingImports=false
"""Improve a skill description based on eval results using OpenCode CLI."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse SKILL.md and return (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")

    name = ""
    description = ""
    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if line.startswith("name:"):
            name = line[len("name:") :].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:") :].strip()
            if value in (">", "|", ">-", "|-"):
                continuation = []
                i += 1
                while i < len(frontmatter_lines) and (
                    frontmatter_lines[i].startswith("  ")
                    or frontmatter_lines[i].startswith("\t")
                ):
                    continuation.append(frontmatter_lines[i].strip())
                    i += 1
                description = " ".join(continuation)
                continue
            description = value.strip('"').strip("'")
        i += 1

    return name, description, content


def _call_opencode(prompt: str, model: str | None, timeout: int = 300) -> str:
    """Run `opencode run` and return text output."""
    cmd = ["opencode", "run", "--format", "json"]
    if model:
        cmd.extend(["--model", model])
    cmd.append(prompt)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"opencode run exited {result.returncode}\nstderr: {result.stderr}"
        )

    text = _extract_text_from_json_stream(result.stdout)
    return text or result.stdout.strip()


def _extract_text_from_json_stream(stdout_text: str) -> str:
    """Extract assistant text from OpenCode JSON stream output."""
    chunks = []
    for raw_line in stdout_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type")

        if event_type == "message.part" and event.get("part", {}).get("type") == "text":
            chunks.append(event["part"].get("text", ""))
            continue

        if event_type == "message":
            for part in event.get("message", {}).get("parts", []):
                if part.get("type") == "text":
                    chunks.append(part.get("text", ""))

    return "".join(chunks).strip()


def improve_description(
    skill_name: str,
    skill_content: str,
    current_description: str,
    eval_results: dict,
    history: list[dict],
    model: str,
    test_results: dict | None = None,
    log_dir: Path | None = None,
    iteration: int | None = None,
) -> str:
    """Call OpenCode to improve description based on eval results."""
    failed_triggers = [
        r for r in eval_results["results"] if r["should_trigger"] and not r["pass"]
    ]
    false_triggers = [
        r for r in eval_results["results"] if not r["should_trigger"] and not r["pass"]
    ]

    train_score = (
        f"{eval_results['summary']['passed']}/{eval_results['summary']['total']}"
    )
    if test_results:
        test_score = (
            f"{test_results['summary']['passed']}/{test_results['summary']['total']}"
        )
        scores_summary = f"Train: {train_score}, Test: {test_score}"
    else:
        scores_summary = f"Train: {train_score}"

    prompt = f"""You are optimizing an OpenCode skill description for a skill named \"{skill_name}\".

The description appears in OpenCode's available_skills list. When a user sends a query, the model decides whether to load the skill based on name + description.

Current description:
<current_description>
\"{current_description}\"
</current_description>

Current scores ({scores_summary}):
<scores_summary>
"""

    if failed_triggers:
        prompt += "FAILED TO TRIGGER (should have triggered but didn't):\n"
        for r in failed_triggers:
            prompt += (
                f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
            )
        prompt += "\n"

    if false_triggers:
        prompt += "FALSE TRIGGERS (triggered but should not have):\n"
        for r in false_triggers:
            prompt += (
                f'  - "{r["query"]}" (triggered {r["triggers"]}/{r["runs"]} times)\n'
            )
        prompt += "\n"

    if history:
        prompt += "PREVIOUS ATTEMPTS (avoid repeating same structure):\n\n"
        for h in history:
            train_s = f"{h.get('train_passed', h.get('passed', 0))}/{h.get('train_total', h.get('total', 0))}"
            test_s = (
                f"{h.get('test_passed', '?')}/{h.get('test_total', '?')}"
                if h.get("test_passed") is not None
                else None
            )
            score_str = f"train={train_s}" + (f", test={test_s}" if test_s else "")
            prompt += f"<attempt {score_str}>\n"
            prompt += f'Description: "{h["description"]}"\n'
            if "results" in h:
                prompt += "Train results:\n"
                for r in h["results"]:
                    status = "PASS" if r["pass"] else "FAIL"
                    prompt += f'  [{status}] "{r["query"][:80]}" (triggered {r["triggers"]}/{r["runs"]})\n'
            if h.get("note"):
                prompt += f'Note: {h["note"]}\n'
            prompt += "</attempt>\n\n"

    prompt += f"""</scores_summary>

Skill content:
<skill_content>
{skill_content}
</skill_content>

Write an improved description that generalizes from failures and avoids overfitting to specific prompts.

Requirements:
- 100-200 words preferred
- Hard limit: 1024 characters
- Use imperative style (for example: "Use this skill when...")
- Focus on user intent, not implementation details
- Keep it distinctive compared to other skills

Respond with ONLY the description wrapped in <new_description>...</new_description>.
"""

    text = _call_opencode(prompt, model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = (
        match.group(1).strip().strip('"') if match else text.strip().strip('"')
    )

    transcript = {
        "iteration": iteration,
        "prompt": prompt,
        "response": text,
        "parsed_description": description,
        "char_count": len(description),
        "over_limit": len(description) > 1024,
    }

    if len(description) > 1024:
        shorten_prompt = (
            f"{prompt}\n\n"
            f"---\n\n"
            f"A previous attempt produced this description ({len(description)} chars), "
            f"which exceeds 1024:\n\n"
            f'"{description}"\n\n'
            f"Rewrite it under 1024 characters while preserving key intent coverage. "
            f"Respond only with <new_description>...</new_description>."
        )
        shorten_text = _call_opencode(shorten_prompt, model)
        match = re.search(
            r"<new_description>(.*?)</new_description>", shorten_text, re.DOTALL
        )
        shortened = (
            match.group(1).strip().strip('"')
            if match
            else shorten_text.strip().strip('"')
        )

        transcript["rewrite_prompt"] = shorten_prompt
        transcript["rewrite_response"] = shorten_text
        transcript["rewrite_description"] = shortened
        transcript["rewrite_char_count"] = len(shortened)
        description = shortened

    transcript["final_description"] = description

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"improve_iter_{iteration or 'unknown'}.json"
        log_file.write_text(json.dumps(transcript, indent=2))

    return description


def main():
    parser = argparse.ArgumentParser(
        description="Improve a skill description based on eval results"
    )
    parser.add_argument(
        "--eval-results",
        required=True,
        help="Path to eval results JSON (from run_eval.py)",
    )
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--history", default=None, help="Path to history JSON (previous attempts)"
    )
    parser.add_argument("--model", required=True, help="Model for improvement")
    parser.add_argument(
        "--verbose", action="store_true", help="Print progress to stderr"
    )
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    eval_results = json.loads(Path(args.eval_results).read_text())
    history = []
    if args.history:
        history = json.loads(Path(args.history).read_text())

    name, _, content = parse_skill_md(skill_path)
    current_description = eval_results["description"]

    if args.verbose:
        print(f"Current: {current_description}", file=sys.stderr)
        print(
            f"Score: {eval_results['summary']['passed']}/{eval_results['summary']['total']}",
            file=sys.stderr,
        )

    new_description = improve_description(
        skill_name=name,
        skill_content=content,
        current_description=current_description,
        eval_results=eval_results,
        history=history,
        model=args.model,
    )

    if args.verbose:
        print(f"Improved: {new_description}", file=sys.stderr)

    output = {
        "description": new_description,
        "history": history
        + [
            {
                "description": current_description,
                "passed": eval_results["summary"]["passed"],
                "failed": eval_results["summary"]["failed"],
                "total": eval_results["summary"]["total"],
                "results": eval_results["results"],
            }
        ],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
