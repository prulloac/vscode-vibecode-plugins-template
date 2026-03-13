#!/usr/bin/env bash
# Commit message validation hook using OpenCode CLI.
# Sources validate-commit-msg-common.sh for shared logic.

CLI_NAME="opencode"
COMMIT_MSG_FILE="$1"

# Check that opencode is available
if ! command -v opencode &>/dev/null; then
    echo "WARNING: opencode not found, skipping commit message validation"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

validate_with_cli() {
    local prompt="$1"

    # Run opencode in JSON mode and extract the text response
    local raw
    raw=$(opencode run --format json "$prompt" 2>/dev/null || true)

    # Parse: find the "text" event and extract its .text field
    OUTPUT=$(echo "$raw" | while IFS= read -r line; do
        if echo "$line" | grep -q '"type":"text"'; then
            echo "$line" | sed 's/.*"text":"\(.*\)","time".*/\1/'
            break
        fi
    done)

    # Unescape newlines from JSON
    OUTPUT=$(echo "$OUTPUT" | sed 's/\\n/\n/g')
}

source "$SCRIPT_DIR/validate-commit-msg-common.sh"
