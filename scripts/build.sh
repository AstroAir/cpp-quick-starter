#!/usr/bin/env bash
# Cross-platform build script for cpp-quick-starter
# Usage: ./build.sh [preset] [--clean] [--target TARGET] [--jobs N]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default values
PRESET=""
CLEAN=false
TARGET=""
JOBS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --jobs|-j)
            JOBS="$2"
            shift 2
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

echo "========================================"
echo "  Building with preset: $PRESET"
echo "========================================"

# Clean if requested
if [[ "$CLEAN" == "true" ]]; then
    echo "Cleaning build directory..."
    rm -rf "$PROJECT_ROOT/build"
fi

# Configure
echo ""
echo "Configuring..."
cmake --preset "$PRESET"

# Build
echo ""
echo "Building..."
BUILD_ARGS=(--build --preset "$PRESET")
if [[ -n "$TARGET" ]]; then
    BUILD_ARGS+=(--target "$TARGET")
fi
if [[ -n "$JOBS" ]]; then
    BUILD_ARGS+=(-j "$JOBS")
fi

cmake "${BUILD_ARGS[@]}"

echo ""
echo "Build completed successfully!"
