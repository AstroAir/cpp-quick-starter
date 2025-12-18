#!/usr/bin/env python3
"""
cpp-quick-starter CLI - Main entry point.
A beautiful and interactive scaffolding tool for C++ projects.

Usage:
    python -m cli init          Initialize a new project
    python -m cli add module    Add a new module
    python -m cli add dep       Add a dependency
    python -m cli info          Show project information
    python -m cli doctor        Check development environment
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List

from . import __version__
from .ui import (
    print_banner,
    print_box,
    print_list,
    print_success,
    print_error,
    print_warning,
    print_info,
    cyan,
    green,
    yellow,
    red,
    dim,
    bold,
    magenta,
    Symbols,
    Spinner,
    set_color_enabled,
)
from . import prompts
from .commands import (
    cmd_init,
    cmd_add_module,
    cmd_add_dependency,
    cmd_strip_language,
    detect_project_info,
)


def cmd_info(root: Optional[Path] = None) -> bool:
    """Show project information."""
    if root is None:
        root = Path.cwd()

    root = root.resolve()

    project_info = detect_project_info(root)

    if not project_info:
        print_error("Could not detect project information.")
        print_info("Are you in a cpp-quick-starter project directory?")
        return False

    print_banner(
        project_info["name"],
        f"Project Information",
        "",
    )

    # Detect features
    features = []
    if (root / "CMakeLists.txt").exists():
        features.append(f"{green(Symbols.SUCCESS)} CMake")
    if (root / "xmake.lua").exists():
        features.append(f"{green(Symbols.SUCCESS)} xmake")
    if (root / "vcpkg.json").exists():
        features.append(f"{green(Symbols.SUCCESS)} vcpkg")
    if (root / "conanfile.txt").exists():
        features.append(f"{green(Symbols.SUCCESS)} Conan")
    if (root / "tests").exists():
        features.append(f"{green(Symbols.SUCCESS)} Tests")
    if (root / "benchmarks").exists():
        features.append(f"{green(Symbols.SUCCESS)} Benchmarks")
    if (root / "docs").exists():
        features.append(f"{green(Symbols.SUCCESS)} Documentation")

    print_box(
        [
            f"Name:       {cyan(project_info['name'])}",
            f"Root:       {cyan(str(root))}",
            f"Include:    {cyan('include/' + project_info['header_dir'] + '/')}",
        ],
        title="Project",
    )

    print()
    print(f"  {bold('Features:')}")
    for feature in features:
        print(f"    {feature}")

    # Count files
    src_files = list((root / "src").rglob("*.cpp")) if (root / "src").exists() else []
    header_files = (
        list((root / "include").rglob("*.hpp")) if (root / "include").exists() else []
    )
    test_files = (
        list((root / "tests").rglob("*.cpp")) if (root / "tests").exists() else []
    )

    print()
    print_box(
        [
            f"Source files:  {cyan(str(len(src_files)))}",
            f"Header files:  {cyan(str(len(header_files)))}",
            f"Test files:    {cyan(str(len(test_files)))}",
        ],
        title="Statistics",
    )

    return True


def cmd_doctor(root: Optional[Path] = None) -> bool:
    """Check development environment."""
    import shutil
    import subprocess

    print_banner(
        "Environment Doctor",
        "Checking your development environment",
        "",
    )

    tools = [
        ("cmake", "CMake", True, "Build system"),
        ("ninja", "Ninja", False, "Fast build tool"),
        ("g++", "GCC", False, "GNU C++ Compiler"),
        ("clang++", "Clang", False, "LLVM C++ Compiler"),
        ("cl", "MSVC", False, "Microsoft C++ Compiler"),
        ("xmake", "xmake", False, "Build system"),
        ("vcpkg", "vcpkg", False, "Package manager"),
        ("conan", "Conan", False, "Package manager"),
        ("clang-format", "clang-format", False, "Code formatter"),
        ("clang-tidy", "clang-tidy", False, "Static analyzer"),
        ("cppcheck", "cppcheck", False, "Static analyzer"),
        ("doxygen", "Doxygen", False, "Documentation generator"),
        ("mkdocs", "MkDocs", False, "Documentation generator"),
        ("git", "Git", True, "Version control"),
        ("python", "Python", True, "Scripting"),
    ]

    print(f"  {bold('Required Tools:')}")
    all_required = True
    for cmd, name, required, desc in tools:
        if not required:
            continue

        found = shutil.which(cmd) is not None

        if found:
            print(f"    {green(Symbols.SUCCESS)} {name} {dim(f'- {desc}')}")
        else:
            print(f"    {red(Symbols.ERROR)} {name} {dim(f'- {desc}')} {red('[MISSING]')}")
            all_required = False

    print()
    print(f"  {bold('Optional Tools:')}")
    compiler_found = False
    for cmd, name, required, desc in tools:
        if required:
            continue

        found = shutil.which(cmd) is not None

        if cmd in ("g++", "clang++", "cl"):
            if found:
                compiler_found = True

        if found:
            print(f"    {green(Symbols.SUCCESS)} {name} {dim(f'- {desc}')}")
        else:
            print(f"    {yellow(Symbols.CIRCLE)} {name} {dim(f'- {desc}')}")

    print()

    if not compiler_found:
        print_error("No C++ compiler found!")
        print_info("Install GCC, Clang, or MSVC to compile C++ code.")
        all_required = False

    if all_required:
        print_success("All required tools are available!")
        print()
        print_box(
            [
                f"cmake --preset ninja-debug",
                f"cmake --build --preset ninja-debug",
                f"ctest --preset ninja-debug",
            ],
            title="Quick Start",
        )
    else:
        print_error("Some required tools are missing!")
        print()
        print_info("Installation suggestions:")
        print_list(
            [
                "Windows: Install Visual Studio with C++ workload",
                "Linux: sudo apt install build-essential cmake ninja-build",
                "macOS: xcode-select --install && brew install cmake ninja",
            ]
        )

    return all_required


def cmd_help() -> None:
    """Show help information."""
    print_banner(
        "C++ Quick Starter CLI",
        "Modern C++20 Project Scaffolding",
        __version__,
    )

    print(f"  {bold('Usage:')}")
    print(f"    {cyan('cqs')} {dim('<command>')} {dim('[options]')}")
    print()

    print(f"  {bold('Commands:')}")
    commands = [
        ("init", "Initialize a new project interactively"),
        ("add module", "Add a new module/component"),
        ("add dep", "Add a package dependency"),
        ("strip en", "Remove English from bilingual docs"),
        ("strip zh", "Remove Chinese from bilingual docs"),
        ("info", "Show project information"),
        ("doctor", "Check development environment"),
        ("help", "Show this help message"),
    ]
    for cmd, desc in commands:
        print(f"    {cyan(cmd.ljust(12))} {desc}")

    print()
    print(f"  {bold('Examples:')}")
    print(f"    {dim('$')} cqs init")
    print(f"    {dim('$')} cqs add module")
    print(f"    {dim('$')} cqs add dep fmt")
    print()

    print(f"  {bold('Options:')}")
    print(f"    {cyan('--no-color')}    Disable colored output")
    print(f"    {cyan('--version')}     Show version number")
    print(f"    {cyan('--help')}        Show help")
    print()


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point."""
    if args is None:
        args = sys.argv[1:]

    # Handle global flags
    if "--no-color" in args:
        set_color_enabled(False)
        args.remove("--no-color")

    if "--version" in args or "-v" in args:
        print(f"cpp-quick-starter CLI v{__version__}")
        return 0

    if not args or args[0] in ("--help", "-h", "help"):
        cmd_help()
        return 0

    command = args[0]

    try:
        if command == "init":
            quick = "--quick" in args or "-q" in args
            success = cmd_init(quick=quick)
            return 0 if success else 1

        elif command == "add":
            if len(args) < 2:
                print_error("Missing subcommand. Use 'add module' or 'add dep'.")
                return 1

            subcommand = args[1]
            if subcommand in ("module", "mod", "m"):
                success = cmd_add_module()
                return 0 if success else 1
            elif subcommand in ("dep", "dependency", "d", "pkg", "package"):
                success = cmd_add_dependency()
                return 0 if success else 1
            else:
                print_error(f"Unknown subcommand: {subcommand}")
                print_info("Available: module, dep")
                return 1

        elif command == "info":
            success = cmd_info()
            return 0 if success else 1

        elif command == "doctor":
            success = cmd_doctor()
            return 0 if success else 1

        elif command == "strip":
            if len(args) < 2:
                print_error("Missing language. Use 'strip en' or 'strip zh'.")
                return 1

            lang = args[1].lower()
            if lang not in ("en", "zh", "english", "chinese"):
                print_error(f"Unknown language: {lang}")
                print_info("Available: en (English), zh (Chinese)")
                return 1

            # Normalize language
            if lang in ("english", "en"):
                lang = "en"
            else:
                lang = "zh"

            success = cmd_strip_language(lang=lang)
            return 0 if success else 1

        else:
            print_error(f"Unknown command: {command}")
            print_info("Run 'cqs help' for available commands.")
            return 1

    except KeyboardInterrupt:
        print()
        print_warning("Aborted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
