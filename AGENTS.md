# AGENTS.md

## General Agentic Guidelines

### Handling Uncertainty

- When uncertain about requirements, ask clarifying questions before proceeding
- If a task is ambiguous, propose a reasonable interpretation and confirm before implementing
- Admit knowledge limitations rather than guessing incorrectly

### Avoiding Training Biases

- Prioritize using existing skills and tools over improvisation
- When a skill exists for a task, use it instead of inventing new approaches
- Follow established project conventions rather than assuming best practices

### Multi-Step Tasks

- Use in-memory todo lists for tasks requiring more than 2 steps
- Track progress through complex workflows
- Complete tasks in logical order, handling dependencies appropriately

### Output Formats

- Respect explicit agent-to-human output formats when specified
- Do not omit required output structures from agents or subagents
- Follow any documented response conventions for this project

## Code Review

- Review code changes for correctness, security, and performance
- Check that code follows project conventions and style
- Verify lint/typecheck passes before marking review complete
- Ensure tests are included for new functionality

## Code Generation

- Write clear, readable code that matches existing patterns
- Include appropriate comments for complex logic
- Ensure generated code is secure and follows best practices
- Test generated code to verify it works correctly

## Guidelines for AI Agents

1. **Use existing skills** when available rather than reinventing workflows
1. **Follow project conventions** - match the existing code style
1. **Run lint/typecheck** before completing significant changes
1. **Commit responsibly** - use the `git-commit-workflow` skill for commits
1. **Test changes** when applicable
1. **Never commit secrets** - avoid committing `.env`, credentials, or keys
