#!/usr/bin/env bash
# Cross-platform code formatting script
# Usage: ./format.sh [--check] [--verbose]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

CHECK=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            CHECK=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

if ! command -v clang-format >/dev/null 2>&1; then
    echo "Error: clang-format not found in PATH" >&2
    echo "Install clang-format or add it to PATH" >&2
    exit 1
fi

echo "Using: $(command -v clang-format)"

# Find source files
EXTENSIONS=("cpp" "hpp" "h" "cc" "cxx" "hxx")
DIRECTORIES=("include" "src" "tests" "benchmarks" "examples")

files=()
for dir in "${DIRECTORIES[@]}"; do
    dir_path="$PROJECT_ROOT/$dir"
    if [[ -d "$dir_path" ]]; then
        for ext in "${EXTENSIONS[@]}"; do
            while IFS= read -r -d '' file; do
                files+=("$file")
            done < <(find "$dir_path" -name "*.$ext" -type f -print0 2>/dev/null)
        done
    fi
done

if [[ ${#files[@]} -eq 0 ]]; then
    echo "No source files found"
    exit 0
fi

echo "Found ${#files[@]} files to format"

has_changes=false

if [[ "$CHECK" == "true" ]]; then
    for file in "${files[@]}"; do
        if [[ "$VERBOSE" == "true" ]]; then
            echo "  Checking: $(basename "$file")"
        fi
        if ! clang-format --dry-run --Werror "$file" 2>/dev/null; then
            echo "  Needs formatting: $file"
            has_changes=true
        fi
    done

    if [[ "$has_changes" == "true" ]]; then
        echo ""
        echo "Some files need formatting. Run: ./scripts/format.sh"
        exit 1
    else
        echo ""
        echo "All files are properly formatted"
    fi
else
    for file in "${files[@]}"; do
        if [[ "$VERBOSE" == "true" ]]; then
            echo "  Formatting: $(basename "$file")"
        fi
        clang-format -i "$file"
    done
    echo ""
    echo "Formatted ${#files[@]} files"
fi
