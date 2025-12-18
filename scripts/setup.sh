#!/usr/bin/env bash
# Cross-platform setup and dependency check script
# Usage: ./setup.sh [--verbose]

set -euo pipefail

VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
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

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

check_tool() {
    local name="$1"
    local command="${2:-$1}"
    local required="${3:-false}"

    if command -v "$command" >/dev/null 2>&1; then
        printf "  ${GREEN}[OK]${NC} %s" "$name"
        if [[ "$VERBOSE" == "true" ]]; then
            local version
            version=$("$command" --version 2>&1 | head -n1) || version=""
            printf " - %s" "$version"
        fi
        printf "\n"
        return 0
    else
        if [[ "$required" == "true" ]]; then
            printf "  ${RED}[MISSING]${NC} %s [Required]\n" "$name"
        else
            printf "  ${YELLOW}[missing]${NC} %s [Optional]\n" "$name"
        fi
        return 1
    fi
}

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  cpp-quick-starter Setup${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# System info
echo -e "${YELLOW}System Information:${NC}"
echo "  OS: $(uname -s) $(uname -r)"
echo "  Arch: $(uname -m)"
echo ""

# Required tools
echo -e "${YELLOW}Required Tools:${NC}"
all_required=true
check_tool "CMake" "cmake" true || all_required=false

# Check for C++ compiler
compiler_found=false
check_tool "g++" "g++" false && compiler_found=true
check_tool "clang++" "clang++" false && compiler_found=true
if [[ "$compiler_found" == "false" ]]; then
    echo -e "  ${RED}[MISSING]${NC} C++ compiler (g++ or clang++) [Required]"
    all_required=false
fi

# Build tools
echo ""
echo -e "${YELLOW}Build Tools:${NC}"
check_tool "Ninja" "ninja" || true
check_tool "xmake" "xmake" || true
check_tool "Make" "make" || true

# Package managers
echo ""
echo -e "${YELLOW}Package Managers:${NC}"
check_tool "vcpkg" "vcpkg" || true
check_tool "Conan" "conan" || true

# Code quality
echo ""
echo -e "${YELLOW}Code Quality Tools:${NC}"
check_tool "clang-format" "clang-format" || true
check_tool "clang-tidy" "clang-tidy" || true
check_tool "cppcheck" "cppcheck" || true

# Documentation
echo ""
echo -e "${YELLOW}Documentation Tools:${NC}"
check_tool "Doxygen" "doxygen" || true
check_tool "MkDocs" "mkdocs" || true
check_tool "Python" "python3" || check_tool "Python" "python" || true
check_tool "uv" "uv" || true

# Version control
echo ""
echo -e "${YELLOW}Version Control:${NC}"
check_tool "Git" "git" true || all_required=false
check_tool "pre-commit" "pre-commit" || true

echo ""
echo -e "${CYAN}========================================${NC}"

if [[ "$all_required" == "true" ]]; then
    echo -e "  ${GREEN}All required tools are available!${NC}"
    echo ""
    echo -e "${YELLOW}Quick Start:${NC}"
    echo "  cmake --preset ninja-debug"
    echo "  cmake --build --preset ninja-debug"
    echo "  ctest --preset ninja-debug"
else
    echo -e "  ${RED}Some required tools are missing!${NC}"
    echo ""
    echo -e "${YELLOW}Installation suggestions:${NC}"
    if [[ "$(uname -s)" == "Darwin" ]]; then
        echo "  xcode-select --install"
        echo "  brew install cmake ninja"
    else
        echo "  Ubuntu/Debian: sudo apt install build-essential cmake ninja-build"
        echo "  Fedora: sudo dnf install gcc-c++ cmake ninja-build"
        echo "  Arch: sudo pacman -S base-devel cmake ninja"
    fi
fi

echo -e "${CYAN}========================================${NC}"
