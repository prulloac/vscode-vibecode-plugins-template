#!/usr/bin/env bash
# Commit message validation hook using GitHub Copilot CLI (standalone).
# Sources validate-commit-msg-common.sh for shared logic.

CLI_NAME="copilot"
COMMIT_MSG_FILE="$1"

# Check that copilot is available
if ! command -v copilot &>/dev/null; then
    echo "WARNING: copilot not found, skipping commit message validation"
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

validate_with_cli() {
    local prompt="$1"

    # Run copilot in non-interactive silent mode (plain text output)
    OUTPUT=$(copilot -p "$prompt" --silent 2>/dev/null || true)
}

source "$SCRIPT_DIR/validate-commit-msg-common.sh"
