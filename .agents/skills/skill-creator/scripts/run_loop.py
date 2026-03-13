#!/usr/bin/env python3
# pyright: reportMissingImports=false
"""Run eval + improve loop for skill description optimization."""

import argparse
import json
import random
import subprocess
import sys
import tempfile
import time
import webbrowser
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_report import generate_html
from improve_description import improve_description
from run_eval import find_project_root, run_eval


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


def split_eval_set(
    eval_set: list[dict], holdout: float, seed: int = 42
) -> tuple[list[dict], list[dict]]:
    """Split eval set into train/test with stratification by should_trigger."""
    random.seed(seed)

    trigger = [e for e in eval_set if e["should_trigger"]]
    no_trigger = [e for e in eval_set if not e["should_trigger"]]

    random.shuffle(trigger)
    random.shuffle(no_trigger)

    n_trigger_test = max(1, int(len(trigger) * holdout)) if trigger else 0
    n_no_trigger_test = max(1, int(len(no_trigger) * holdout)) if no_trigger else 0

    test_set = trigger[:n_trigger_test] + no_trigger[:n_no_trigger_test]
    train_set = trigger[n_trigger_test:] + no_trigger[n_no_trigger_test:]
    if not train_set:
        train_set, test_set = test_set, []

    return train_set, test_set


def run_loop(
    eval_set: list[dict],
    skill_path: Path,
    description_override: str | None,
    num_workers: int,
    timeout: int,
    max_iterations: int,
    runs_per_query: int,
    trigger_threshold: float,
    holdout: float,
    model: str,
    verbose: bool,
    live_report_path: Path | None = None,
    log_dir: Path | None = None,
) -> dict:
    """Run iterative evaluate/improve loop."""
    _ = find_project_root()
    name, original_description, content = parse_skill_md(skill_path)
    current_description = description_override or original_description

    if holdout > 0:
        train_set, test_set = split_eval_set(eval_set, holdout)
    else:
        train_set = eval_set
        test_set = []

    history = []
    exit_reason = "unknown"

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"Iteration {iteration}/{max_iterations}", file=sys.stderr)

        all_queries = train_set + test_set
        all_results = run_eval(
            eval_set=all_queries,
            skill_name=name,
            description=current_description,
            num_workers=num_workers,
            timeout=timeout,
            project_root=skill_path.parent.parent.parent.parent,
            runs_per_query=runs_per_query,
            trigger_threshold=trigger_threshold,
            model=model,
        )

        train_queries = {q["query"] for q in train_set}
        train_result_list = [
            r for r in all_results["results"] if r["query"] in train_queries
        ]
        test_result_list = [
            r for r in all_results["results"] if r["query"] not in train_queries
        ]

        train_passed = sum(1 for r in train_result_list if r["pass"])
        train_total = len(train_result_list)
        test_passed = (
            sum(1 for r in test_result_list if r["pass"]) if test_set else None
        )
        test_total = len(test_result_list) if test_set else None

        train_results = {
            "results": train_result_list,
            "summary": {
                "passed": train_passed,
                "failed": train_total - train_passed,
                "total": train_total,
            },
        }

        test_results = None
        if test_set:
            test_results = {
                "results": test_result_list,
                "summary": {
                    "passed": test_passed,
                    "failed": test_total - test_passed,
                    "total": test_total,
                },
            }

        history.append(
            {
                "iteration": iteration,
                "description": current_description,
                "train_passed": train_passed,
                "train_failed": train_total - train_passed,
                "train_total": train_total,
                "train_results": train_result_list,
                "test_passed": test_passed,
                "test_failed": (test_total - test_passed) if test_set else None,
                "test_total": test_total,
                "test_results": test_result_list if test_set else None,
                "passed": train_passed,
                "failed": train_total - train_passed,
                "total": train_total,
                "results": train_result_list,
            }
        )

        if live_report_path:
            partial = {
                "original_description": original_description,
                "best_description": current_description,
                "best_score": "in progress",
                "iterations_run": len(history),
                "holdout": holdout,
                "train_size": len(train_set),
                "test_size": len(test_set),
                "history": history,
            }
            live_report_path.write_text(
                generate_html(partial, auto_refresh=True, skill_name=name)
            )

        if train_total > 0 and train_passed == train_total:
            exit_reason = f"all_passed (iteration {iteration})"
            break

        if iteration == max_iterations:
            exit_reason = f"max_iterations ({max_iterations})"
            break

        blinded_history = [
            {k: v for k, v in h.items() if not k.startswith("test_")} for h in history
        ]
        current_description = improve_description(
            skill_name=name,
            skill_content=content,
            current_description=current_description,
            eval_results=train_results,
            history=blinded_history,
            model=model,
            test_results=test_results,
            log_dir=log_dir,
            iteration=iteration,
        )

    if test_set:
        best = max(history, key=lambda h: h.get("test_passed") or 0)
        best_score = f"{best['test_passed']}/{best['test_total']}"
        best_test_score = best_score
    else:
        best = max(history, key=lambda h: h.get("train_passed", 0))
        best_score = f"{best['train_passed']}/{best['train_total']}"
        best_test_score = None

    return {
        "exit_reason": exit_reason,
        "original_description": original_description,
        "best_description": best["description"],
        "best_score": best_score,
        "best_train_score": f"{best['train_passed']}/{best['train_total']}",
        "best_test_score": best_test_score,
        "final_description": current_description,
        "iterations_run": len(history),
        "holdout": holdout,
        "train_size": len(train_set),
        "test_size": len(test_set),
        "history": history,
    }


def open_path(path: Path):
    """Best-effort open path in default browser."""
    try:
        webbrowser.open(str(path))
        return
    except Exception:
        pass
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Run eval + improve loop")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument(
        "--description", default=None, help="Override starting description"
    )
    parser.add_argument(
        "--num-workers", type=int, default=8, help="Number of parallel workers"
    )
    parser.add_argument(
        "--timeout", type=int, default=60, help="Timeout per query in seconds"
    )
    parser.add_argument(
        "--max-iterations", type=int, default=5, help="Max improvement iterations"
    )
    parser.add_argument("--runs-per-query", type=int, default=3, help="Runs per query")
    parser.add_argument(
        "--trigger-threshold", type=float, default=0.5, help="Trigger threshold"
    )
    parser.add_argument("--holdout", type=float, default=0.4, help="Holdout fraction")
    parser.add_argument("--model", required=True, help="Model for improvement")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    parser.add_argument("--report", default="auto", help="Report path, auto, or none")
    parser.add_argument("--results-dir", default=None, help="Directory to save outputs")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, _, _ = parse_skill_md(skill_path)

    if args.report != "none":
        if args.report == "auto":
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            live_report_path = (
                Path(tempfile.gettempdir())
                / f"skill_description_report_{skill_path.name}_{timestamp}.html"
            )
        else:
            live_report_path = Path(args.report)
        live_report_path.write_text(
            "<html><body><h1>Starting optimization loop...</h1></body></html>"
        )
        open_path(live_report_path)
    else:
        live_report_path = None

    if args.results_dir:
        timestamp = time.strftime("%Y-%m-%d_%H%M%S")
        results_dir = Path(args.results_dir) / timestamp
        results_dir.mkdir(parents=True, exist_ok=True)
    else:
        results_dir = None

    log_dir = results_dir / "logs" if results_dir else None

    output = run_loop(
        eval_set=eval_set,
        skill_path=skill_path,
        description_override=args.description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        max_iterations=args.max_iterations,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        holdout=args.holdout,
        model=args.model,
        verbose=args.verbose,
        live_report_path=live_report_path,
        log_dir=log_dir,
    )

    json_output = json.dumps(output, indent=2)
    print(json_output)

    if results_dir:
        (results_dir / "results.json").write_text(json_output)
    if live_report_path:
        live_report_path.write_text(
            generate_html(output, auto_refresh=False, skill_name=name)
        )
    if results_dir and live_report_path:
        (results_dir / "report.html").write_text(
            generate_html(output, auto_refresh=False, skill_name=name)
        )


if __name__ == "__main__":
    main()
