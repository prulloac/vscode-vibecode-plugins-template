---
name: task-complexity-assessor
description: Use this skill when a user requests a new feature, bug fix, refactoring, or any multi-step task. Assesses complexity, estimates steps, determines if a todo list is needed, and suggests relevant skills to accomplish the task.
---

# Task Complexity Assessor Skill

**Answers the question: Is this task complex enough to warrant a todo list? Which skills might help?**

This skill evaluates task complexity and recommends the appropriate planning approach.

## When to Use

Use this skill when a user requests:

- A new feature implementation
- A bug fix requiring multiple steps
- A refactoring task
- Any multi-step task or project
- Help with a complex problem

**Key indicator**: User asks for something that will require more than one action to complete.

## How It Works

### Step 1: Analyze the Request

Evaluate the user's request by considering:

- **Number of distinct components** - How many files or systems are involved?
- **Prerequisites** - Are there dependencies or setup steps required?
- **Testing** - Will tests need to be written?
- **Documentation** - Are docs or README updates needed?
- **Configuration** - Are there config changes required?
- **Integration** - Does this connect with other systems?

### Step 2: Estimate Complexity

Categorize the task:

| Complexity | Indicators | Steps Estimate |
|------------|------------|----------------|
| Simple | Single file, one change, no tests | 1-2 steps |
| Moderate | Few files, some testing, basic config | 3-5 steps |
| Complex | Multiple files, full test suite, docs, config | 6-10 steps |
| Very Complex | Many files, system-wide changes, migrations | 10+ steps |

### Step 3: Determine Todo Requirement

- **≤3 steps**: Proceed directly without todo list
- **>3 steps**: Create a todo list to track progress

### Step 4: Scan for Relevant Skills

Discover available skills dynamically by examining their frontmatter. See [## Discovering Available Skills](#discovering-available-skills) for the full discovery procedure. Recommend the top 2-3 most relevant skills based on description matching.

## Discovering Available Skills

Skills are not a fixed list — they grow over time. Always discover them dynamically at assessment time.

### Where to Find Skills

Skills are typically located in one of these directories (check in order):

1. `.agents/skills/` — project-level skills for agents (most common)
2. `.opencode/skills/` — project-level skills for OpenCode
3. `~/.agents/skills/` — user-level skills

Each skill directory follows this structure:

```
<skills-dir>/
├── skill-name/
│   ├── SKILL.md          # Main skill definition (includes YAML frontmatter)
│   └── references/       # Optional reference docs
└── ...
```

### How to Discover Skills

**Step 1 — List all skill directories across all supported locations:**

```bash
for dir in .agents/skills .opencode/skills ~/.agents/skills; do
  [ -d "$dir" ] && echo "=== $dir ===" && ls "$dir"
done
```

**Step 2 — Read each skill's frontmatter to understand its purpose:**

```bash
head -n 20 <skills-dir>/<skill-name>/SKILL.md
```

Replace `<skills-dir>` with whichever directory the skill was found in (e.g., `.agents/skills` or `.opencode/skills`).

The frontmatter (between `---` delimiters) contains:
- `name`: the skill identifier
- `description`: a concise explanation of what the skill does and when to use it

Example output:
```
---
name: feature-breakdown
description: Analyze feature specifications and decompose them into core components,
  individual tasks, and acceptance criteria. Use when you have a feature spec/idea
  and need to identify ALL the work required...
---
```

**Step 3 — Match skill descriptions to the task at hand:**

Read the `description` field carefully. It typically includes:
- What the skill does
- When it should be used (look for phrases like "Use when…")
- What inputs it expects (e.g., "when you have a feature spec")

Select the 2–3 skills whose descriptions best align with the user's request.

## Output Format

After assessment, provide:

```markdown
## Task Complexity Assessment

**Task**: [User's request summary]

**Complexity Rating**: [Simple|Moderate|Complex|Very Complex]
**Estimated Steps**: [N] steps

### Todo Recommendation
[Use a todo list / Proceed without todo list]

### Relevant Skills
Based on the task, consider these skills:
1. **[Skill Name]**: [Why it's relevant]
2. **[Skill Name]**: [Why it's relevant]
3. **[Skill Name]**: [Why it's relevant]

### Recommended Approach
[High-level strategy for tackling this task]
```

## Workflow Integration

When you assess a task:

1. **Load this skill** to analyze complexity
2. **Follow the assessment steps** above
3. **If todo recommended**:
   - Create and maintain an in-memory todo list for this task
   - Break down the task into individual steps
   - Mark each step with priority (high/medium/low)
4. **If skills recommended**:
   - Suggest loading relevant skills to the user
   - Explain how each skill helps

## Safe Execution

When assessment requires external operations (for example, listing skill directories or reading many skill files), apply these safeguards:

1. **Use explicit error handling**
   - Wrap file and subprocess operations in `try/except`.
   - On failure, report a concise, non-sensitive message and continue with partial results when possible.
   - If a required path is missing or unreadable, mark that source as unavailable and proceed with remaining sources.

2. **Set timeout expectations for long-running operations**
   - Apply timeouts to subprocess and network calls.
   - Recommended default: `30s` per external command/request.
   - If a timeout occurs, stop that operation, report timeout status, and continue with available data.

3. **Fail safely and transparently**
   - Never guess missing data from failed operations.
   - Explicitly state which checks were completed vs skipped due to errors/timeouts.
   - Keep all behavior read-only; do not modify files or repositories during assessment.

## Examples

### Example 1: Simple Task (No Todo)

**User Request**: "Fix the typo in the README"

- Analysis: Single file, one change
- Complexity: Simple
- Steps: 1
- **Recommendation**: Proceed without todo list

### Example 2: Complex Task (Use Todo)

**User Request**: "Add user authentication to the app"

- Analysis: Multiple files, database, config, tests, docs
- Complexity: Complex
- Steps: 8+
- **Recommendation**: Create todo list
- **Relevant Skills**:
  - `feature-breakdown` - Decompose authentication into tasks
  - `github-workflows` - Add auth-related CI workflows
  - `skill-creator` - If creating auth-related skills

### Example 3: Moderate Task (Use Todo)

**User Request**: "Create a new GitHub workflow for deployments"

- Analysis: Single system, but requires workflow file, tests, docs
- Complexity: Moderate
- Steps: 4
- **Recommendation**: Create todo list
- **Relevant Skills**:
  - `github-workflows` - Create/modify workflows
  - `skill-validator` - If creating a deployment skill

## Key Principles

1. **Be conservative** - When in doubt, recommend a todo list
2. **Think ahead** - Consider not just immediate steps but testing, docs, config
3. **Match skills wisely** - Only recommend skills that genuinely apply
4. **Explain reasoning** - Help the user understand the complexity assessment
5. **Be actionable** - Provide concrete next steps

## Common Pitfalls to Avoid

❌ **Underestimating complexity** - "It looks simple" often leads to scope creep

❌ **Missing relevant skills** - Not scanning available skills thoroughly

❌ **Over-recommending todo** - Simple tasks don't need overhead

❌ **Vague recommendations** - "Consider using skills" is not helpful; be specific

## Validation

After completing the assessment, verify:

- [ ] Complexity rating is one of: Simple / Moderate / Complex / Very Complex
- [ ] Estimated step count aligns with the complexity table
- [ ] Todo recommendation is explicitly stated (use / skip)
- [ ] 2–3 relevant skills are named with justification (or explicitly none if N/A)
- [ ] Output follows the format defined in "## Output Format"
