#!/usr/bin/env bash
# Shared logic for commit message validation hooks.
# Sourced by the CLI-specific wrappers (opencode, copilot, gemini).
#
# Expects the caller to set:
#   COMMIT_MSG_FILE  -> path to the commit message file (passed as $1 by pre-commit)
#   CLI_NAME         -> name of the CLI for log messages
#   validate_with_cli "$PROMPT"  -> function that sets $OUTPUT with the agent's text response

set -euo pipefail

COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Skip merge/revert commits
if [[ "$COMMIT_MSG" =~ ^(Merge|Revert) ]]; then
    exit 0
fi

PROJECT_ROOT=$(git rev-parse --show-toplevel)
CONTRIBUTING=$(cat "$PROJECT_ROOT/CONTRIBUTING.md" 2>/dev/null || true)

PROMPT="You are a commit message validator. Your ONLY job is to check if the following commit message complies with the commit message guidelines defined in this project's CONTRIBUTING.md.

The commit message to validate:
---
$COMMIT_MSG
---

The project's CONTRIBUTING.md:
---
$CONTRIBUTING
---

Rules:
1. Do NOT use any tools. Do NOT read any files. Do NOT run any commands.
2. Look for commit message guidelines in the CONTRIBUTING.md above. Validate the message against whatever convention the project defines.
3. Only if CONTRIBUTING.md does not define any commit message convention, fall back to the Conventional Commits specification:
   - Format: <type>(<scope>): <subject>
   - Valid types: feat, fix, docs, style, refactor, test, chore, perf, ci
   - Lowercase type and scope
   - Subject line under 72 characters
   - Imperative mood in subject (\"add\" not \"added\")
   - Blank line between subject and body (if body exists)
4. Your response MUST start with exactly PASS or FAIL on the first line.
5. On the following lines, give a brief explanation (1-3 sentences max).
6. Do not output anything else."

# Call the CLI-specific validation function
validate_with_cli "$PROMPT"

# Check the result
FIRST_WORD=$(echo "$OUTPUT" | head -c 4)

if [ "$FIRST_WORD" = "PASS" ]; then
    echo "commit-msg: validated by $CLI_NAME"
    exit 0
elif [ "$FIRST_WORD" = "FAIL" ]; then
    echo "commit-msg: rejected by $CLI_NAME"
    echo ""
    echo "$OUTPUT"
    echo ""
    echo "See CONTRIBUTING.md for commit message guidelines."
    exit 1
else
    echo "WARNING: $CLI_NAME returned an unclear response, letting commit through"
    exit 0
fi
