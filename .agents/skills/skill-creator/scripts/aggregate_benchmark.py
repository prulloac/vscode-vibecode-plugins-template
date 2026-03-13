#!/usr/bin/env python3
"""Aggregate per-run grading into benchmark summary files."""

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path


def calculate_stats(values):
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    n = len(values)
    mean = sum(values) / n
    stddev = 0.0
    if n > 1:
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        stddev = math.sqrt(variance)
    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_run_results(iteration_dir: Path):
    results = {}
    for eval_dir in sorted(iteration_dir.glob("eval-*")):
        try:
            eval_id = int(eval_dir.name.split("-")[1])
        except (ValueError, IndexError):
            continue

        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            config = config_dir.name
            if config not in results:
                results[config] = []

            for run_dir in sorted(config_dir.glob("run-*")):
                grading_file = run_dir / "grading.json"
                if not grading_file.exists():
                    continue
                grading = json.loads(grading_file.read_text())

                timing_file = run_dir / "timing.json"
                timing = (
                    json.loads(timing_file.read_text()) if timing_file.exists() else {}
                )

                try:
                    run_number = int(run_dir.name.split("-")[1])
                except (ValueError, IndexError):
                    run_number = 1

                result = {
                    "eval_id": eval_id,
                    "configuration": config,
                    "run_number": run_number,
                    "result": {
                        "pass_rate": grading.get("summary", {}).get("pass_rate", 0.0),
                        "passed": grading.get("summary", {}).get("passed", 0),
                        "failed": grading.get("summary", {}).get("failed", 0),
                        "total": grading.get("summary", {}).get("total", 0),
                        "time_seconds": timing.get("total_duration_seconds", 0.0),
                        "tokens": timing.get("total_tokens", 0),
                        "tool_calls": grading.get("execution_metrics", {}).get(
                            "total_tool_calls", 0
                        ),
                        "errors": grading.get("execution_metrics", {}).get(
                            "errors_encountered", 0
                        ),
                    },
                    "expectations": grading.get("expectations", []),
                    "notes": [],
                }
                results[config].append(result)
    return results


def build_summary(results):
    run_summary = {}
    config_names = sorted(results.keys())
    for config in config_names:
        rows = results[config]
        pass_rates = [r["result"]["pass_rate"] for r in rows]
        times = [r["result"]["time_seconds"] for r in rows]
        tokens = [r["result"]["tokens"] for r in rows]
        run_summary[config] = {
            "pass_rate": calculate_stats(pass_rates),
            "time_seconds": calculate_stats(times),
            "tokens": calculate_stats(tokens),
        }

    if len(config_names) >= 2:
        primary = run_summary[config_names[0]]
        baseline = run_summary[config_names[1]]
        run_summary["delta"] = {
            "pass_rate": f"{primary['pass_rate']['mean'] - baseline['pass_rate']['mean']:+.2f}",
            "time_seconds": f"{primary['time_seconds']['mean'] - baseline['time_seconds']['mean']:+.1f}",
            "tokens": f"{primary['tokens']['mean'] - baseline['tokens']['mean']:+.0f}",
        }
    else:
        run_summary["delta"] = {
            "pass_rate": "+0.00",
            "time_seconds": "+0.0",
            "tokens": "+0",
        }

    return run_summary


def main():
    parser = argparse.ArgumentParser(description="Aggregate benchmark runs")
    parser.add_argument("iteration_dir", help="Path to iteration directory")
    parser.add_argument("--skill-name", default="skill")
    args = parser.parse_args()

    iteration_dir = Path(args.iteration_dir)
    results = load_run_results(iteration_dir)

    runs = []
    for config, rows in results.items():
        runs.extend(rows)

    benchmark = {
        "metadata": {
            "skill_name": args.skill_name,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": sorted({r["eval_id"] for r in runs}),
            "runs_per_configuration": max((r["run_number"] for r in runs), default=1),
        },
        "runs": sorted(
            runs, key=lambda r: (r["eval_id"], r["configuration"], r["run_number"])
        ),
        "run_summary": build_summary(results),
        "notes": [],
    }

    output_json = iteration_dir / "benchmark.json"
    output_md = iteration_dir / "benchmark.md"
    output_json.write_text(json.dumps(benchmark, indent=2))

    lines = [f"# Benchmark: {args.skill_name}", "", "## Summary", ""]
    for config, summary in benchmark["run_summary"].items():
        if config == "delta":
            continue
        lines.append(
            f"- {config}: pass_rate={summary['pass_rate']['mean']:.2f}, time={summary['time_seconds']['mean']:.2f}s, tokens={summary['tokens']['mean']:.0f}"
        )
    lines.append("")
    lines.append(f"- delta pass_rate: {benchmark['run_summary']['delta']['pass_rate']}")
    lines.append(
        f"- delta time_seconds: {benchmark['run_summary']['delta']['time_seconds']}"
    )
    lines.append(f"- delta tokens: {benchmark['run_summary']['delta']['tokens']}")
    output_md.write_text("\n".join(lines) + "\n")

    print(f"Generated: {output_json}")
    print(f"Generated: {output_md}")


if __name__ == "__main__":
    main()
