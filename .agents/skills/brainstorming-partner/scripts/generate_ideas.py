#!/usr/bin/env python3
"""
Brainstorming idea generator using six frameworks.

Generates ideas using:
1. SCAMPER (Substitute, Combine, Adapt, Modify, Put to other uses, Eliminate, Reverse)
2. Six Thinking Hats (White, Red, Black, Yellow, Green, Blue)
3. Mind Mapping (hierarchical organization of ideas)
4. Lateral Thinking (random word association)
5. Divergence-Convergence (pure generation phase)
6. Forced Connections (combining with external concepts)

Usage:
    python generate_ideas.py "Your brainstorming topic or challenge" [--output ideas.json]

Output:
    JSON file with ideas grouped by framework, including source framework and description.
"""

import argparse
import json
import random
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class Idea:
    """Represents a single generated idea."""

    id: str
    framework: str
    title: str
    description: str
    thinking_mode: str  # e.g., "SCAMPER: Substitute", "Six Hats: Red Hat", etc.


def generate_scamper_ideas(topic: str, context: str = "") -> List[Idea]:
    """Generate ideas using SCAMPER framework."""
    ideas = []
    scamper_modes = {
        "Substitute": f"What components or elements in {topic} could be replaced or substituted?",
        "Combine": f"How could {topic} be combined with other ideas, services, or products?",
        "Adapt": f"What could be adjusted or adapted in {topic} to serve other purposes?",
        "Modify": f"What could be magnified, minimized, or otherwise modified in {topic}?",
        "Put to other uses": f"How could {topic} be repurposed or used for different applications?",
        "Eliminate": f"What could be removed, simplified, or eliminated from {topic}?",
        "Reverse": f"What could be done in reverse order or inverted in {topic}?",
    }

    for mode, question in scamper_modes.items():
        ideas.append(
            Idea(
                id=f"scamper_{mode.lower().replace(' ', '_')}",
                framework="SCAMPER",
                title=f"SCAMPER: {mode}",
                description=question,
                thinking_mode=f"SCAMPER: {mode}",
            )
        )

    return ideas


def generate_six_hats_ideas(topic: str, context: str = "") -> List[Idea]:
    """Generate ideas using Six Thinking Hats framework."""
    ideas = []
    hats = {
        "White": f"What facts and data do we know about {topic}? What information is missing?",
        "Red": f"What's our emotional/intuitive reaction to {topic}? What feels right or wrong?",
        "Black": f"What could go wrong with {topic}? What are the risks and problems?",
        "Yellow": f"What's the best case scenario for {topic}? What are the benefits and opportunities?",
        "Green": f"What creative alternatives exist for {topic}? How could we innovate here?",
        "Blue": f"How should we organize and proceed with {topic}? What's the plan?",
    }

    for hat, question in hats.items():
        ideas.append(
            Idea(
                id=f"sixhats_{hat.lower()}",
                framework="Six Thinking Hats",
                title=f"Six Hats: {hat} Hat",
                description=question,
                thinking_mode=f"Six Thinking Hats: {hat} Hat",
            )
        )

    return ideas


def generate_mind_mapping_ideas(topic: str, context: str = "") -> List[Idea]:
    """Generate ideas using Mind Mapping framework."""
    ideas = []

    # Central theme and primary branches
    branches = {
        "Problem & Root Causes": f"What are the underlying problems and root causes driving {topic}?",
        "Stakeholders & Perspectives": f"Who are the stakeholders in {topic}? What are their perspectives?",
        "Current Solutions": f"What solutions already exist for {topic}? How do they work?",
        "Resources & Constraints": f"What resources are available for {topic}? What constraints exist?",
        "Desired Outcomes": f"What are the ideal outcomes or goals for {topic}?",
        "Interconnections": f"How does {topic} connect to other areas or systems?",
    }

    for branch, question in branches.items():
        ideas.append(
            Idea(
                id=f"mindmap_{branch.lower().replace(' ', '_').replace('&', 'and')}",
                framework="Mind Mapping",
                title=f"Mind Map: {branch}",
                description=question,
                thinking_mode=f"Mind Mapping: {branch}",
            )
        )

    return ideas


def generate_lateral_thinking_ideas(topic: str, context: str = "") -> List[Idea]:
    """Generate ideas using Lateral Thinking / Random Word Association."""
    ideas = []

    # Random unrelated concepts to force connections
    random_concepts = [
        "ocean waves",
        "chess game",
        "garden",
        "jazz music",
        "mirror",
        "library",
        "storm",
        "river",
        "marketplace",
        "telescope",
        "beehive",
        "clock",
        "volcano",
        "forest",
        "bridge",
    ]

    selected_concepts = random.sample(random_concepts, min(5, len(random_concepts)))

    for i, concept in enumerate(selected_concepts):
        ideas.append(
            Idea(
                id=f"lateral_{i}_{concept.replace(' ', '_')}",
                framework="Lateral Thinking",
                title=f"Lateral: Force Connection with '{concept}'",
                description=f"How could insights from '{concept}' apply to {topic}? What unexpected connections exist?",
                thinking_mode=f"Lateral Thinking: Random Word Association ({concept})",
            )
        )

    return ideas


def generate_divergence_convergence_ideas(topic: str, context: str = "") -> List[Idea]:
    """Generate ideas using Divergence-Convergence framework."""
    ideas = []

    # Divergence prompts (no evaluation)
    divergence_prompts = [
        f"Generate free-flowing ideas about {topic} without any judgment or constraints.",
        f"What would {topic} look like if we had unlimited resources and no restrictions?",
        f"If we could completely reimagine {topic}, what would we create?",
        f"What if the opposite of current {topic} approaches was true? What ideas emerge?",
        f"Combine the wildest ideas you can think of related to {topic}.",
        f"What {topic} ideas would excite and inspire people most?",
    ]

    for i, prompt in enumerate(divergence_prompts):
        ideas.append(
            Idea(
                id=f"divergence_{i}",
                framework="Divergence-Convergence",
                title=f"Divergence Prompt {i+1}",
                description=prompt,
                thinking_mode=f"Divergence-Convergence: Pure Generation (Prompt {i+1})",
            )
        )

    return ideas


def generate_forced_connections_ideas(topic: str, context: str = "") -> List[Idea]:
    """Generate ideas using Forced Connections framework."""
    ideas = []

    # External domains to force connections with
    external_domains = [
        "e-commerce platforms",
        "healthcare systems",
        "aerospace engineering",
        "sports coaching",
        "film production",
        "urban planning",
        "culinary arts",
        "game design",
        "education systems",
        "natural ecosystems",
    ]

    selected_domains = random.sample(external_domains, min(4, len(external_domains)))

    for i, domain in enumerate(selected_domains):
        ideas.append(
            Idea(
                id=f"forced_{i}_{domain.replace(' ', '_')}",
                framework="Forced Connections",
                title=f"Forced Connection: {domain}",
                description=f"How could principles, practices, or concepts from '{domain}' be applied to {topic}? What novel combinations emerge?",
                thinking_mode=f"Forced Connections: {domain}",
            )
        )

    return ideas


def main():
    """Main entry point for idea generation."""
    parser = argparse.ArgumentParser(
        description="Generate brainstorming ideas using six frameworks"
    )
    parser.add_argument("topic", help="The brainstorming topic or challenge")
    parser.add_argument(
        "--context",
        default="",
        help="Additional context or constraints for the brainstorming",
    )
    parser.add_argument(
        "--output",
        default="ideas.json",
        help="Output JSON file path (default: ideas.json)",
    )

    args = parser.parse_args()

    # Generate ideas from all frameworks
    all_ideas = []

    all_ideas.extend(generate_scamper_ideas(args.topic, args.context))
    all_ideas.extend(generate_six_hats_ideas(args.topic, args.context))
    all_ideas.extend(generate_mind_mapping_ideas(args.topic, args.context))
    all_ideas.extend(generate_lateral_thinking_ideas(args.topic, args.context))
    all_ideas.extend(generate_divergence_convergence_ideas(args.topic, args.context))
    all_ideas.extend(generate_forced_connections_ideas(args.topic, args.context))

    # Group by framework
    ideas_by_framework = {}
    for idea in all_ideas:
        if idea.framework not in ideas_by_framework:
            ideas_by_framework[idea.framework] = []
        ideas_by_framework[idea.framework].append(asdict(idea))

    # Prepare output
    output = {
        "metadata": {
            "topic": args.topic,
            "context": args.context,
            "generated_at": datetime.now().isoformat(),
            "total_ideas": len(all_ideas),
            "frameworks_used": list(ideas_by_framework.keys()),
        },
        "ideas_by_framework": ideas_by_framework,
        "all_ideas": [asdict(idea) for idea in all_ideas],
    }

    # Write to file
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Generated {len(all_ideas)} ideas using 6 frameworks")
    print(f"📊 Frameworks: {', '.join(ideas_by_framework.keys())}")
    print(f"💾 Saved to: {args.output}")
    print(f"\nIdeas by framework:")
    for framework, ideas in ideas_by_framework.items():
        print(f"  - {framework}: {len(ideas)} ideas")


if __name__ == "__main__":
    main()
