---
name: brainstorming-partner
description: Brainstorm ideas with a reliable AI partner using proven frameworks and evaluations. Triggers for topics requiring idea generation, problem-solving, innovation, feature ideation, strategic planning, or creative exploration. Combines SCAMPER, Six Thinking Hats, Mind Mapping, Lateral Thinking, Divergence-Convergence, and Forced Connections frameworks with Feasibility/Impact/Novelty evaluation to assess and rank ideas before presenting them for interactive refinement.
---

# Brainstorming Partner

## Overview

Brainstorming Partner is an interactive skill that helps you generate, evaluate, and refine ideas using multiple proven brainstorming frameworks. Instead of brainstorming alone, you get a reliable AI partner that applies six distinct frameworks to your challenge, evaluates each idea's feasibility, impact, and novelty, and presents ranked results for iterative refinement.

**Use this skill when you need to:**

- Generate innovative ideas for products, features, or services
- Solve complex business or technical problems
- Explore multiple perspectives on a challenge
- Evaluate ideas before committing resources
- Have structured idea-generation conversations with AI assistance

## Brainstorming Workflow

### 1. Present Your Challenge

Start by describing what you want to brainstorm. Provide:

- **Topic or Challenge**: The problem, opportunity, or area you want to explore
- **Context**: Any constraints, goals, or background relevant to the brainstorming
- **Desired Outcomes**: What success looks like (optional but helpful)

Example: "I need to brainstorm how to reduce our 40% onboarding drop-off rate. Our users get frustrated during setup. What could we explore?"

### 2. Multi-Framework Idea Generation

The skill applies six complementary frameworks to generate diverse ideas:

- **SCAMPER** - Systematic innovation through substitution, combination, adaptation, modification, repurposing, elimination, and reversal
- **Six Thinking Hats** - Multi-perspective thinking (facts, emotions, risks, benefits, creativity, process)
- **Mind Mapping** - Hierarchical exploration of problems, stakeholders, solutions, and connections
- **Lateral Thinking** - Breaking patterns through random word association and unexpected connections
- **Divergence-Convergence** - Pure generation followed by structured evaluation
- **Forced Connections** - Combining your challenge with concepts from unrelated domains

See `references/frameworks.md` for detailed framework descriptions.

### 3. Idea Evaluation

Each generated idea is evaluated on three dimensions:

- **Feasibility (0-10)**: How practical and actionable is it? Can you actually do it?
- **Impact (0-10)**: How significant and valuable would it be if implemented?
- **Novelty (0-10)**: How original is it? What's the degree of newness?

**Composite Score = (Feasibility + Impact + Novelty) / 3**

See `references/evaluation_metrics.md` for detailed rubrics and scoring guidance.

### 4. Ranked Results & Interactive Iteration

Ideas are ranked by composite score and presented with:

- Individual metric scores with reasoning
- Overall assessment (Strong/Good/Fair/Weak)
- Framework source (which technique generated it)
- Full description

You then iterate: ask for clarification, request refinement, explore specific ideas deeper, or generate new ideas based on feedback.

## Using the Skill with Agents

### Running Idea Generation

Execute the idea generation script:

```bash
python scripts/generate_ideas.py "Your brainstorming topic" \
  --context "Additional context or constraints" \
  --output ideas.json
```

This generates idea prompts across all six frameworks organized by type.

### Evaluating Ideas

Run the evaluation script to score ideas on Feasibility, Impact, and Novelty:

```bash
python scripts/evaluate_ideas.py ideas.json \
  --context "Your context" \
  --topic "Your topic" \
  --output evaluated_ideas.json
```

This produces:

- Individual scores for each metric
- Composite rankings
- Score distribution statistics
- Assessment summary for each idea

### Testing the Skill

Test prompts are available in `evals/evals.json` covering:

- Product feature brainstorming
- Business problem-solving
- Creative campaign ideation
- Technical architecture decisions
- Content strategy
- User experience improvement

## Evaluation Metrics Reference

### Feasibility Scoring

**How practical is the idea given real-world constraints?**

- 9-10: Can implement immediately with existing resources
- 7-8: Achievable with some additional resources or effort
- 5-6: Possible but requires significant effort or new skills
- 3-4: Very difficult; requires major changes or external dependencies
- 1-2: Extremely difficult or unrealistic
- 0: Impossible or violates fundamental constraints

### Impact Scoring

**How valuable and transformative would it be?**

- 9-10: Transformational—solves major problems or creates substantial value
- 7-8: Significant—meaningfully improves the situation
- 5-6: Moderate—provides measurable benefits
- 3-4: Marginal—provides minor improvements
- 1-2: Minimal—barely noticeable impact
- 0: No positive impact or negative effects

### Novelty Scoring

**How original and new is the idea?**

- 9-10: Highly unique—truly novel in this space
- 7-8: Original—significant variation on existing approaches
- 5-6: Somewhat new—adaptation with new elements
- 3-4: Incremental—minor variations on standard approaches
- 1-2: Minimal newness—obvious or widely-used
- 0: Not new—direct copy of existing solutions

### Composite Score Interpretation

- **8-10**: Strong idea—pursue aggressively
- **6-7.9**: Good idea—consider with conditions
- **5-5.9**: Fair idea—useful for specific contexts
- **3-4.9**: Weak idea—needs refinement
- **0-2.9**: Poor idea—unlikely to pursue

## Brainstorming Frameworks

### SCAMPER

Systematically applies seven techniques to existing solutions:

- **Substitute**: Replace components or attributes
- **Combine**: Merge with other products or ideas
- **Adapt**: Adjust for other purposes
- **Modify**: Change form, scale, or attributes
- **Put to other uses**: Repurpose or use differently
- **Eliminate**: Remove or simplify
- **Reverse**: Invert order or direction

**Best for**: Product improvements, process optimization, features addition

### Six Thinking Hats

Uses six thinking modes as "hats" for parallel thinking:

- **White Hat**: Facts and data—what do we know?
- **Red Hat**: Emotions and intuition—what do we feel?
- **Black Hat**: Critical thinking—what could go wrong?
- **Yellow Hat**: Optimism—what's the best case?
- **Green Hat**: Creativity—what else could work?
- **Blue Hat**: Process and organization—how do we proceed?

**Best for**: Complex problems, team decision-making, fair evaluation

### Mind Mapping

Creates hierarchical structure showing relationships:

- Central theme with primary and secondary branches
- Shows problem aspects, stakeholders, solutions, and connections
- Identifies gaps and relationships visually

**Best for**: Breaking down complex topics, exploring relationships, identifying gaps

### Lateral Thinking

Uses random stimuli to break habitual patterns:

- Force connections between unrelated concepts and your challenge
- Explore unexpected associations
- Follow tangential paths to novel solutions

**Best for**: Breaking mental blocks, truly novel ideas, creative problem-solving

### Divergence-Convergence

Separates generation from evaluation:

- **Divergence**: Generate many ideas without judgment
- **Convergence**: Evaluate and filter ideas systematically

**Best for**: Encouraging quantity and novelty, preventing premature judgment

### Forced Connections

Combines unrelated concepts and domains:

- List key attributes of your challenge
- Combine with concepts from different fields
- Explore implications of combinations

**Best for**: Cross-disciplinary innovation, unique positioning, product mashups

## Iterative Refinement

After evaluation, iterate with your partner:

1. **Dive Deeper**: Ask for more details on high-scoring ideas
1. **Combine Ideas**: Merge complementary ideas from different frameworks
1. **Refine Weak Ideas**: Explore how to improve lower-scoring ideas
1. **Explore Trade-offs**: Understand feasibility vs. impact trade-offs
1. **Generate More**: Request additional ideas in specific directions
1. **Prioritize**: Decide which ideas to pursue based on your strategy

Example conversation:

- "Can you elaborate on the top three ideas?"
- "How could we make the high-novelty but low-feasibility ideas more doable?"
- "Which combination of these ideas would be most impactful?"
- "Generate more ideas focused specifically on reducing complexity"

## Core Capabilities

### 1. Multi-Framework Idea Generation

Applies six proven brainstorming frameworks to generate diverse perspectives on your challenge.

### 2. Feasibility-Impact-Novelty Evaluation

Scores each idea on three dimensions to provide balanced assessment of viability and value.

### 3. Ranked Presentation

Ideas ordered by composite score with detailed reasoning for each metric.

### 4. Framework Transparency

Each idea tagged with source framework so you understand which technique generated it.

### 5. Interactive Iteration

Refine ideas, combine approaches, and generate new ideas based on feedback.

### 6. Contextual Adaptation

Frameworks applied flexibly to any brainstorming scenario: products, processes, content, strategy, technical decisions, etc.

## Scripts Reference

### `scripts/generate_ideas.py`

Generates brainstorming ideas using all six frameworks.

**Usage:**

```bash
python generate_ideas.py "Topic or challenge" \
  --context "Additional context" \
  --output ideas.json
```

**Output**: JSON file with ideas organized by framework.

**Parameters:**

- `topic` (required): Your brainstorming topic
- `--context`: Additional constraints or background
- `--output`: Output file path (default: ideas.json)

### `scripts/evaluate_ideas.py`

Evaluates ideas on Feasibility, Impact, and Novelty metrics.

**Usage:**

```bash
python evaluate_ideas.py ideas.json \
  --context "Your context" \
  --output evaluated_ideas.json \
  --min-score 5.0
```

**Output**: JSON file with scored and ranked ideas.

**Parameters:**

- `input_file` (required): Ideas JSON from generate_ideas.py
- `--context`: Context for evaluation
- `--topic`: Original brainstorming topic
- `--output`: Output file path (default: evaluated_ideas.json)
- `--min-score`: Minimum composite score to include (default: 0)

## How to Brainstorm Effectively

### Preparation

1. **Be Specific**: The clearer your challenge, the better the ideas
1. **Provide Context**: Share constraints, goals, and background
1. **Set Expectations**: What does success look like?

### During Brainstorming

1. **Suspend Judgment**: Don't dismiss ideas immediately
1. **Explore All Frameworks**: Each generates different idea types
1. **Look for Patterns**: Which frameworks generate your best ideas?
1. **Combine Ideas**: Often the best solution merges multiple ideas

### After Evaluation

1. **Consider Trade-offs**: High feasibility might mean lower novelty (and vice versa)
1. **Think About Portfolio**: Mix of safe bets + moonshots
1. **Look for Quick Wins**: High feasibility + high impact = immediate action
1. **Identify Refinement**: What would make lower-scoring ideas viable?
1. **Iterate**: The second round often produces better results

## Tips for Better Results

- **More Context Helps**: Include goals, constraints, past attempts, and success criteria
- **Diverse Thinking**: Frameworks generate different idea types; use multiple
- **Combine Frameworks**: Best ideas often come from merging insights from different frameworks
- **Iterate Aggressively**: Refine ideas based on feedback; rarely right the first time
- **Document Reasoning**: Understand *why* ideas scored high helps with implementation
