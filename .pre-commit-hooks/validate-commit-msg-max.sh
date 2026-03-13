#!/usr/bin/env bash
# Commit message validation hook enforcing max subject length.

set -euo pipefail

COMMIT_MSG_FILE=""
MAX_LENGTH_INPUT="128"

for arg in "$@"; do
    if [[ -f "$arg" ]]; then
        COMMIT_MSG_FILE="$arg"
    elif [[ "$arg" =~ ^[0-9]+$ ]]; then
        MAX_LENGTH_INPUT="$arg"
    fi
done

if [[ -z "$COMMIT_MSG_FILE" || ! -f "$COMMIT_MSG_FILE" ]]; then
    echo "commit-msg: could not read commit message file"
    exit 1
fi

if ! [[ "$MAX_LENGTH_INPUT" =~ ^[0-9]+$ ]] || (( MAX_LENGTH_INPUT <= 0 )); then
    echo "commit-msg: invalid max length '${MAX_LENGTH_INPUT}' (must be a positive integer)"
    exit 1
fi

FIRST_LINE="$(sed -n '1p' "$COMMIT_MSG_FILE")"

# Skip Git-generated merge/revert commits
if [[ "$FIRST_LINE" =~ ^(Merge|Revert) ]]; then
    exit 0
fi

MAX_LENGTH=$MAX_LENGTH_INPUT
if (( ${#FIRST_LINE} > MAX_LENGTH )); then
    echo "commit-msg: rejected (subject line exceeds ${MAX_LENGTH} characters)"
    echo "Length: ${#FIRST_LINE}"
    exit 1
fi

echo "commit-msg: validated (subject line <= ${MAX_LENGTH} chars)"
exit 0
