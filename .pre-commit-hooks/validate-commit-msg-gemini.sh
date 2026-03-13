#!/usr/bin/env bash
# Commit message validation hook using Gemini CLI.
# Sources validate-commit-msg-common.sh for shared logic.

CLI_NAME="gemini"
COMMIT_MSG_FILE="$1"

# Check that gemini is available
if ! command -v gemini &>/dev/null; then
    echo "WARNING: gemini not found, skipping commit message validation"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

validate_with_cli() {
    local prompt="$1"

    # Run gemini in non-interactive mode with JSON output
    local raw
    raw=$(gemini -p "$prompt" -o json 2>/dev/null || true)

    # Parse the JSON response to extract text content
    # Gemini JSON output contains response objects; extract the text
    if command -v jq &>/dev/null; then
        OUTPUT=$(echo "$raw" | jq -r '
            .[] | select(.type == "response") | .response // empty
        ' 2>/dev/null || echo "$raw")
    else
        # Fallback: try to extract text without jq
        # Gemini JSON typically has the response text in a "response" field
        OUTPUT=$(echo "$raw" | sed 's/.*"response":"\(.*\)".*/\1/' | sed 's/\\n/\n/g' 2>/dev/null || echo "$raw")
    fi
}

source "$SCRIPT_DIR/validate-commit-msg-common.sh"
