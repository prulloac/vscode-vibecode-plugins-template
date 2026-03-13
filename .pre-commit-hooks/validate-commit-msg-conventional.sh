#!/usr/bin/env bash
# Commit message validation hook using Conventional Commits regex rules.

set -euo pipefail

COMMIT_MSG_FILE="${1:-}"

if [[ -z "$COMMIT_MSG_FILE" || ! -f "$COMMIT_MSG_FILE" ]]; then
    echo "commit-msg: could not read commit message file"
    exit 1
fi

COMMIT_MSG="$(cat "$COMMIT_MSG_FILE")"
FIRST_LINE="$(printf '%s' "$COMMIT_MSG" | sed -n '1p')"

# Skip Git-generated merge/revert commits
if [[ "$FIRST_LINE" =~ ^(Merge|Revert) ]]; then
    exit 0
fi

# Conventional Commits:
# <type>(<scope>)?!: <description>
# scope is optional and lowercase if present.
CONVENTIONAL_REGEX='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9][a-z0-9._/-]*\))?(!)?: .+$'

if ! [[ "$FIRST_LINE" =~ $CONVENTIONAL_REGEX ]]; then
    echo "commit-msg: rejected (does not match Conventional Commits)"
    echo
    echo "Expected: <type>(<scope>)?: <subject>"
    echo "Example: feat(auth): add OAuth login"
    echo "Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    exit 1
fi

if (( ${#FIRST_LINE} > 72 )); then
    echo "commit-msg: rejected (subject line must be 72 chars or fewer)"
    exit 1
fi

# If a body exists, require a blank line between subject and body.
if [[ "$COMMIT_MSG" == *$'\n'* ]]; then
    SECOND_LINE="$(printf '%s' "$COMMIT_MSG" | sed -n '2p')"
    if [[ -n "$SECOND_LINE" ]]; then
        echo "commit-msg: rejected (add a blank line between subject and body)"
        exit 1
    fi
fi

echo "commit-msg: validated by conventional regex"
exit 0
