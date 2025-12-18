#!/usr/bin/env bash
# Cross-platform clean script for cpp-quick-starter
# Usage: ./clean.sh [--all] [--build-only]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

ALL=false
BUILD_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all|-a)
            ALL=true
            shift
            ;;
        --build-only|-b)
            BUILD_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Colors
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Cleaning project${NC}"
echo -e "${CYAN}========================================${NC}"

# Directories to remove
dirs_to_remove=("build")

if [[ "$BUILD_ONLY" != "true" ]]; then
    dirs_to_remove+=(".xmake" ".cache")
fi

if [[ "$ALL" == "true" ]]; then
    dirs_to_remove+=(".vscode/.cache" ".idea")
fi

# Files to remove
files_to_remove=("compile_commands.json")

for dir in "${dirs_to_remove[@]}"; do
    dir_path="$PROJECT_ROOT/$dir"
    if [[ -d "$dir_path" ]]; then
        echo -e "  ${YELLOW}Removing:${NC} $dir"
        rm -rf "$dir_path"
    fi
done

for file in "${files_to_remove[@]}"; do
    file_path="$PROJECT_ROOT/$file"
    if [[ -f "$file_path" ]]; then
        echo -e "  ${YELLOW}Removing:${NC} $file"
        rm -f "$file_path"
    fi
done

echo ""
echo -e "${GREEN}Cleaned successfully!${NC}"
