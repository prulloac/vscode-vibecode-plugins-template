# JSON Schemas

This document defines JSON structures used by this skill's eval workflow.

## evals.json

Located at `evals/evals.json` inside the target skill directory.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "Output includes required field X",
        "Output format is correct"
      ]
    }
  ]
}
```

## grading.json

Located at `<run-dir>/grading.json`.

```json
{
  "expectations": [
    {
      "text": "Output includes required field X",
      "passed": true,
      "evidence": "Found in output file summary"
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 0,
    "total": 1,
    "pass_rate": 1.0
  }
}
```

Important: viewer tooling expects `text`, `passed`, and `evidence` keys exactly.

## timing.json

Located at `<run-dir>/timing.json`.

```json
{
  "total_tokens": 12000,
  "duration_ms": 24000,
  "total_duration_seconds": 24.0
}
```

## benchmark.json

Located at `<iteration-dir>/benchmark.json`.

```json
{
  "metadata": {
    "skill_name": "example-skill",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2],
    "runs_per_configuration": 3
  },
  "runs": [
    {
      "eval_id": 1,
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 1.0,
        "passed": 2,
        "failed": 0,
        "total": 2,
        "time_seconds": 10.2,
        "tokens": 2400,
        "tool_calls": 12,
        "errors": 0
      },
      "expectations": [
        {
          "text": "Output includes required field X",
          "passed": true,
          "evidence": "Found in output"
        }
      ],
      "notes": []
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 1.0, "stddev": 0.0, "min": 1.0, "max": 1.0},
      "time_seconds": {"mean": 10.2, "stddev": 0.0, "min": 10.2, "max": 10.2},
      "tokens": {"mean": 2400, "stddev": 0.0, "min": 2400, "max": 2400}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.5, "stddev": 0.0, "min": 0.5, "max": 0.5},
      "time_seconds": {"mean": 8.5, "stddev": 0.0, "min": 8.5, "max": 8.5},
      "tokens": {"mean": 1800, "stddev": 0.0, "min": 1800, "max": 1800}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+1.7",
      "tokens": "+600"
    }
  },
  "notes": []
}
```
