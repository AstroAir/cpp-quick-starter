#!/usr/bin/env bash
# Cross-platform test runner script
# Usage: ./test.sh [preset] [--filter PATTERN] [--verbose] [--build]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

PRESET=""
FILTER=""
VERBOSE=false
BUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --filter|-f)
            FILTER="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --build|-b)
            BUILD=true
            shift
            ;;
        -*)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        *)
            PRESET="$1"
            shift
            ;;
    esac
done

# Determine default preset
if [[ -z "$PRESET" ]]; then
    PRESET="ninja-debug"
fi

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Running tests with preset: $PRESET${NC}"
echo -e "${CYAN}========================================${NC}"

# Build if requested
if [[ "$BUILD" == "true" ]]; then
    echo ""
    echo "Building..."
    cmake --preset "$PRESET"
    cmake --build --preset "$PRESET"
fi

# Run tests
echo ""
echo "Running tests..."
TEST_ARGS=(--preset "$PRESET" --output-on-failure)

if [[ "$VERBOSE" == "true" ]]; then
    TEST_ARGS+=(--verbose)
fi

if [[ -n "$FILTER" ]]; then
    TEST_ARGS+=(-R "$FILTER")
fi

if ctest "${TEST_ARGS[@]}"; then
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
