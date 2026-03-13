#!/usr/bin/env python3
"""
Idea evaluator using Feasibility, Impact, and Novelty metrics.

Evaluates generated ideas based on:
- Feasibility (0-10): How practical and actionable
- Impact (0-10): How significant and valuable
- Novelty (0-10): How original and new

Usage:
    python evaluate_ideas.py ideas.json [--output evaluated_ideas.json]

Input format:
    JSON file with ideas (from generate_ideas.py or custom format)

Output format:
    JSON file with evaluated ideas, scores, and rankings
"""

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class IdeaEvaluation:
    """Represents an evaluated idea with scores."""

    idea_id: str
    title: str
    description: str
    framework: str
    feasibility_score: float  # 0-10
    impact_score: float  # 0-10
    novelty_score: float  # 0-10
    composite_score: float  # Average of three
    feasibility_reasoning: str
    impact_reasoning: str
    novelty_reasoning: str
    overall_assessment: str


def evaluate_idea(
    idea_id: str,
    title: str,
    description: str,
    framework: str,
    context: str = "",
    topic: str = "",
) -> IdeaEvaluation:
    """
    Evaluate a single idea on Feasibility, Impact, and Novelty.

    This is a placeholder for LLM integration. In actual use, these scores
    would come from an LLM evaluation agent.
    """

    # Base scoring logic (simplified for demo)
    # In production, this would call an LLM

    # Feasibility: How complex is the idea in the description?
    feasibility = 6.0
    if any(
        word in description.lower() for word in ["simple", "easy", "straightforward"]
    ):
        feasibility = 8.0
    elif any(
        word in description.lower() for word in ["complex", "difficult", "challenging"]
    ):
        feasibility = 4.0

    feasibility_reasoning = "Based on complexity indicators in the idea description. LLM evaluation recommended for accuracy."

    # Impact: How transformational does it sound?
    impact = 6.0
    if any(
        word in description.lower()
        for word in ["transform", "revolutionize", "major", "significant"]
    ):
        impact = 8.0
    elif any(
        word in description.lower() for word in ["minor", "marginal", "small", "slight"]
    ):
        impact = 3.0

    impact_reasoning = "Based on impact language in the description. LLM evaluation recommended for contextual assessment."

    # Novelty: Framework-based heuristic
    novelty = 6.0
    novel_frameworks = ["Lateral Thinking", "Forced Connections", "Six Thinking Hats"]
    if any(f in framework for f in novel_frameworks):
        novelty = 7.5
    if "SCAMPER" in framework:
        novelty = 5.0

    novelty_reasoning = f"Based on framework type (higher for divergent frameworks). {framework} typically generates ideas with novelty score ~{novelty}."

    # Composite score
    composite = (feasibility + impact + novelty) / 3

    # Overall assessment
    if composite >= 8:
        assessment = "Strong idea—pursue aggressively"
    elif composite >= 6:
        assessment = "Good idea—consider pursuing with conditions"
    elif composite >= 5:
        assessment = "Fair idea—useful for specific contexts"
    else:
        assessment = "Weak idea—may need refinement"

    return IdeaEvaluation(
        idea_id=idea_id,
        title=title,
        description=description,
        framework=framework,
        feasibility_score=round(feasibility, 1),
        impact_score=round(impact, 1),
        novelty_score=round(novelty, 1),
        composite_score=round(composite, 1),
        feasibility_reasoning=feasibility_reasoning,
        impact_reasoning=impact_reasoning,
        novelty_reasoning=novelty_reasoning,
        overall_assessment=assessment,
    )


def load_ideas(filepath: str) -> List[Dict]:
    """Load ideas from JSON file."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)

        # Handle both direct idea lists and structured format
        if isinstance(data, list):
            return data
        elif "all_ideas" in data:
            return data["all_ideas"]
        elif "ideas" in data:
            return data["ideas"]
        else:
            return list(data.values()) if isinstance(data, dict) else []
    except Exception as e:
        print(f"❌ Error loading ideas: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for idea evaluation."""
    parser = argparse.ArgumentParser(
        description="Evaluate brainstorming ideas on Feasibility, Impact, and Novelty"
    )
    parser.add_argument(
        "input_file", help="Input JSON file with ideas (from generate_ideas.py)"
    )
    parser.add_argument(
        "--output",
        default="evaluated_ideas.json",
        help="Output JSON file path (default: evaluated_ideas.json)",
    )
    parser.add_argument(
        "--context", default="", help="Additional context for evaluation"
    )
    parser.add_argument("--topic", default="", help="Original brainstorming topic")
    parser.add_argument(
        "--min-score",
        type=float,
        default=0,
        help="Minimum composite score to include in output (default: 0)",
    )

    args = parser.parse_args()

    # Load ideas
    ideas = load_ideas(args.input_file)

    if not ideas:
        print("❌ No ideas found in input file", file=sys.stderr)
        sys.exit(1)

    # Evaluate each idea
    evaluations = []
    for idea in ideas:
        eval_result = evaluate_idea(
            idea_id=idea.get("id", "unknown"),
            title=idea.get("title", "Untitled"),
            description=idea.get("description", ""),
            framework=idea.get("framework", "Unknown"),
            context=args.context,
            topic=args.topic,
        )
        evaluations.append(asdict(eval_result))

    # Filter by minimum score if specified
    if args.min_score > 0:
        evaluations = [e for e in evaluations if e["composite_score"] >= args.min_score]

    # Sort by composite score (descending)
    evaluations.sort(key=lambda x: x["composite_score"], reverse=True)

    # Calculate statistics
    if evaluations:
        avg_feasibility = sum(e["feasibility_score"] for e in evaluations) / len(
            evaluations
        )
        avg_impact = sum(e["impact_score"] for e in evaluations) / len(evaluations)
        avg_novelty = sum(e["novelty_score"] for e in evaluations) / len(evaluations)
        avg_composite = sum(e["composite_score"] for e in evaluations) / len(
            evaluations
        )
    else:
        avg_feasibility = avg_impact = avg_novelty = avg_composite = 0

    # Prepare output
    output = {
        "metadata": {
            "evaluated_at": datetime.now().isoformat(),
            "input_file": args.input_file,
            "total_evaluated": len(evaluations),
            "original_count": len(ideas),
            "min_score_filter": args.min_score,
        },
        "statistics": {
            "average_feasibility": round(avg_feasibility, 1),
            "average_impact": round(avg_impact, 1),
            "average_novelty": round(avg_novelty, 1),
            "average_composite": round(avg_composite, 1),
            "score_distribution": {
                "strong_8_plus": len(
                    [e for e in evaluations if e["composite_score"] >= 8]
                ),
                "good_6_to_8": len(
                    [e for e in evaluations if 6 <= e["composite_score"] < 8]
                ),
                "fair_5_to_6": len(
                    [e for e in evaluations if 5 <= e["composite_score"] < 6]
                ),
                "weak_below_5": len(
                    [e for e in evaluations if e["composite_score"] < 5]
                ),
            },
        },
        "evaluations": evaluations,
    }

    # Write to file
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    # Print summary
    print(f"✅ Evaluated {len(evaluations)} ideas")
    print(f"📊 Average scores:")
    print(f"   Feasibility: {avg_feasibility:.1f}/10")
    print(f"   Impact: {avg_impact:.1f}/10")
    print(f"   Novelty: {avg_novelty:.1f}/10")
    print(f"   Composite: {avg_composite:.1f}/10")
    print(f"\n📈 Score distribution:")
    print(
        f"   Strong (8+): {output['statistics']['score_distribution']['strong_8_plus']}"
    )
    print(f"   Good (6-8): {output['statistics']['score_distribution']['good_6_to_8']}")
    print(f"   Fair (5-6): {output['statistics']['score_distribution']['fair_5_to_6']}")
    print(f"   Weak (<5): {output['statistics']['score_distribution']['weak_below_5']}")
    print(f"\n💾 Saved to: {args.output}")


if __name__ == "__main__":
    main()
