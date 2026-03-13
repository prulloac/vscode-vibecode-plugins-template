#!/usr/bin/env python3
"""Generate an HTML report from run_loop.py output."""

import argparse
import html
import json
import sys
from pathlib import Path


def generate_html(data: dict, auto_refresh: bool = False, skill_name: str = "") -> str:
    """Generate HTML report from optimization output."""
    history = data.get("history", [])
    title_prefix = html.escape(skill_name + " - ") if skill_name else ""

    train_queries = []
    test_queries = []
    if history:
        for r in history[0].get("train_results", history[0].get("results", [])):
            train_queries.append(
                {"query": r["query"], "should_trigger": r.get("should_trigger", True)}
            )
        if history[0].get("test_results"):
            for r in history[0].get("test_results", []):
                test_queries.append(
                    {
                        "query": r["query"],
                        "should_trigger": r.get("should_trigger", True),
                    }
                )

    refresh_tag = (
        '    <meta http-equiv="refresh" content="5">\n' if auto_refresh else ""
    )

    html_parts = [
        """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
"""
        + refresh_tag
        + """    <title>"""
        + title_prefix
        + """Skill Description Optimization</title>
    <style>
        body { font-family: Georgia, serif; padding: 20px; background: #faf9f5; color: #141413; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #e8e6dc; padding: 8px; font-size: 12px; }
        th { background: #141413; color: #faf9f5; }
        th.test-col { background: #6a9bcc; }
        .pass { color: #2f6b2f; }
        .fail { color: #b22222; }
    </style>
</head>
<body>
    <h1>"""
        + title_prefix
        + """Skill Description Optimization</h1>
"""
    ]

    html_parts.append(
        f"<p><strong>Original:</strong> {html.escape(data.get('original_description', 'N/A'))}</p>"
    )
    html_parts.append(
        f"<p><strong>Best:</strong> {html.escape(data.get('best_description', 'N/A'))}</p>"
    )

    html_parts.append(
        "<table><thead><tr><th>Iter</th><th>Train</th><th>Test</th><th>Description</th>"
    )
    for q in train_queries:
        html_parts.append(f"<th>{html.escape(q['query'])}</th>")
    for q in test_queries:
        html_parts.append(f"<th class='test-col'>{html.escape(q['query'])}</th>")
    html_parts.append("</tr></thead><tbody>")

    for h in history:
        html_parts.append("<tr>")
        html_parts.append(f"<td>{h.get('iteration', '?')}</td>")
        html_parts.append(
            f"<td>{h.get('train_passed', 0)}/{h.get('train_total', 0)}</td>"
        )
        test_passed = h.get("test_passed")
        test_total = h.get("test_total")
        html_parts.append(
            f"<td>{'' if test_passed is None else f'{test_passed}/{test_total}'}</td>"
        )
        html_parts.append(f"<td>{html.escape(h.get('description', ''))}</td>")

        train_by_query = {
            r["query"]: r for r in h.get("train_results", h.get("results", []))
        }
        test_by_query = {r["query"]: r for r in h.get("test_results", [])}

        for q in train_queries:
            r = train_by_query.get(q["query"], {})
            mark = "✓" if r.get("pass") else "✗"
            cls = "pass" if r.get("pass") else "fail"
            html_parts.append(f"<td class='{cls}'>{mark}</td>")
        for q in test_queries:
            r = test_by_query.get(q["query"], {})
            mark = "✓" if r.get("pass") else "✗"
            cls = "pass" if r.get("pass") else "fail"
            html_parts.append(f"<td class='{cls}'>{mark}</td>")

        html_parts.append("</tr>")

    html_parts.append("</tbody></table></body></html>")
    return "".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML report from run_loop output"
    )
    parser.add_argument(
        "input", help="Path to JSON output from run_loop.py (or - for stdin)"
    )
    parser.add_argument(
        "-o", "--output", default=None, help="Output HTML file (default: stdout)"
    )
    parser.add_argument("--skill-name", default="", help="Skill name in title")
    args = parser.parse_args()

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text())

    html_output = generate_html(data, skill_name=args.skill_name)
    if args.output:
        Path(args.output).write_text(html_output)
    else:
        print(html_output)


if __name__ == "__main__":
    main()
