#!/usr/bin/env python3
"""
Cross-platform project initialization script for cpp-quick-starter template.
This script renames the project and updates all necessary files.
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Optional


# Files to update with new project name
FILES_TO_UPDATE = [
    "CMakeLists.txt",
    "CMakePresets.json",
    "xmake.lua",
    "vcpkg.json",
    "conanfile.txt",
    "mkdocs.yml",
    "README.md",
    "README_CN.md",
    "docs/index.md",
    ".github/workflows/ci.yml",
    ".github/workflows/code-quality.yml",
    ".github/workflows/release.yml",
    "src/main.cpp",
    "examples/example_01.cpp",
    "tests/unit/test_greeting.cpp",
    "tests/unit/test_string_utils.cpp",
    "tests/integration/integration_test.cpp",
    "benchmarks/benchmark_greeting.cpp",
]

# Directories to rename
DIRS_TO_RENAME = [
    "include/project_name",
]

# Template markers
OLD_PROJECT_NAME = "cpp_quick_starter"
OLD_PROJECT_NAME_KEBAB = "cpp-quick-starter"
OLD_PROJECT_NAME_PASCAL = "CppQuickStarter"
OLD_HEADER_DIR = "project_name"


def to_snake_case(name: str) -> str:
    """Convert name to snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower().replace("-", "_").replace(" ", "_")


def to_kebab_case(name: str) -> str:
    """Convert name to kebab-case."""
    return to_snake_case(name).replace("_", "-")


def to_pascal_case(name: str) -> str:
    """Convert name to PascalCase."""
    words = re.split(r"[-_\s]+", name)
    return "".join(word.capitalize() for word in words)


def replace_in_file(file_path: Path, replacements: dict[str, str]) -> bool:
    """Replace all occurrences in a file."""
    if not file_path.exists():
        return False

    try:
        content = file_path.read_text(encoding="utf-8")
        original = content

        for old, new in replacements.items():
            content = content.replace(old, new)

        if content != original:
            file_path.write_text(content, encoding="utf-8")
            return True
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"Warning: Could not process {file_path}: {e}")

    return False


def rename_directory(old_path: Path, new_path: Path) -> bool:
    """Rename a directory."""
    if not old_path.exists():
        return False

    if new_path.exists():
        print(f"Warning: Target directory already exists: {new_path}")
        return False

    try:
        old_path.rename(new_path)
        return True
    except OSError as e:
        print(f"Warning: Could not rename {old_path}: {e}")
        return False


def update_header_includes(root: Path, old_dir: str, new_dir: str) -> int:
    """Update #include directives in source files."""
    count = 0
    extensions = {".cpp", ".hpp", ".h", ".cc", ".cxx", ".hxx"}

    for file_path in root.rglob("*"):
        if file_path.suffix in extensions and file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                new_content = content.replace(
                    f'#include "{old_dir}/', f'#include "{new_dir}/'
                ).replace(f'#include <{old_dir}/', f'#include <{new_dir}/')

                if new_content != content:
                    file_path.write_text(new_content, encoding="utf-8")
                    count += 1
            except (UnicodeDecodeError, PermissionError):
                pass

    return count


def clean_template_files(root: Path, keep_git: bool = True) -> None:
    """Clean template-specific files."""
    files_to_remove = [
        "CHANGELOG.md",  # User should start fresh
    ]

    for file_name in files_to_remove:
        file_path = root / file_name
        if file_path.exists():
            file_path.unlink()
            print(f"  Removed: {file_name}")


def create_fresh_changelog(root: Path, project_name: str) -> None:
    """Create a fresh CHANGELOG.md."""
    changelog = root / "CHANGELOG.md"
    content = f"""# Changelog

All notable changes to {project_name} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project setup from cpp-quick-starter template

"""
    changelog.write_text(content, encoding="utf-8")


def reset_git_history(root: Path) -> None:
    """Reset git history for fresh start."""
    git_dir = root / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
        print("  Removed .git directory")

    # Re-initialize git
    os.system(f'cd "{root}" && git init')
    print("  Initialized fresh git repository")


def init_project(
    project_name: str,
    root: Optional[Path] = None,
    header_dir: Optional[str] = None,
    reset_git: bool = False,
    author: Optional[str] = None,
    description: Optional[str] = None,
) -> bool:
    """Initialize the project with new name."""
    if root is None:
        root = Path(__file__).parent.parent

    root = root.resolve()

    # Generate name variants
    snake_name = to_snake_case(project_name)
    kebab_name = to_kebab_case(project_name)
    pascal_name = to_pascal_case(project_name)
    header_name = header_dir or snake_name

    print(f"\n{'='*60}")
    print(f"  Initializing Project: {project_name}")
    print(f"{'='*60}")
    print(f"  Root directory: {root}")
    print(f"  Snake case:     {snake_name}")
    print(f"  Kebab case:     {kebab_name}")
    print(f"  Pascal case:    {pascal_name}")
    print(f"  Header dir:     {header_name}")
    print(f"{'='*60}\n")

    # Build replacements
    replacements = {
        OLD_PROJECT_NAME: snake_name,
        OLD_PROJECT_NAME_KEBAB: kebab_name,
        OLD_PROJECT_NAME_PASCAL: pascal_name,
        OLD_HEADER_DIR: header_name,
        "CPP_QUICK_STARTER": snake_name.upper(),
    }

    if author:
        replacements["Your Name"] = author
        replacements["AstroAir"] = author

    if description:
        replacements[
            "A modern C++20 project template with best practices for quick project bootstrapping."
        ] = description

    # Update files
    print("Updating project files...")
    updated_count = 0
    for file_rel in FILES_TO_UPDATE:
        file_path = root / file_rel
        if replace_in_file(file_path, replacements):
            print(f"  Updated: {file_rel}")
            updated_count += 1

    # Update header includes in all source files
    print("\nUpdating #include directives...")
    include_count = update_header_includes(root, OLD_HEADER_DIR, header_name)
    print(f"  Updated {include_count} files with new include paths")

    # Rename directories
    print("\nRenaming directories...")
    for dir_rel in DIRS_TO_RENAME:
        old_dir = root / dir_rel
        new_dir = old_dir.parent / header_name
        if rename_directory(old_dir, new_dir):
            print(f"  Renamed: {dir_rel} -> {new_dir.relative_to(root)}")

    # Create fresh changelog
    print("\nCreating fresh CHANGELOG.md...")
    create_fresh_changelog(root, project_name)

    # Reset git if requested
    if reset_git:
        print("\nResetting git history...")
        reset_git_history(root)

    print(f"\n{'='*60}")
    print(f"  Project '{project_name}' initialized successfully!")
    print(f"  Updated {updated_count} files")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("  1. Review the changes")
    print("  2. Update README.md with your project details")
    print("  3. Update LICENSE with your name/organization")
    print("  4. Run: cmake --preset ninja-debug && cmake --build --preset ninja-debug")
    print("  5. Commit your changes")
    print()

    return True


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize cpp-quick-starter template with your project name",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python init-project.py MyAwesomeLib
  python init-project.py "My Project" --header-dir myproject
  python init-project.py MyLib --author "John Doe" --reset-git
        """,
    )

    parser.add_argument(
        "project_name", help="Name of your project (e.g., MyAwesomeLib, my-project)"
    )
    parser.add_argument(
        "--header-dir",
        help="Name for the include directory (default: snake_case of project name)",
    )
    parser.add_argument("--author", help="Author name to use in files")
    parser.add_argument("--description", help="Project description")
    parser.add_argument(
        "--reset-git",
        action="store_true",
        help="Reset git history for fresh start",
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Project root directory (default: parent of scripts/)",
    )

    args = parser.parse_args()

    # Validate project name
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_\- ]*$", args.project_name):
        print(
            "Error: Project name must start with a letter and contain only "
            "letters, numbers, underscores, hyphens, or spaces.",
            file=sys.stderr,
        )
        return 1

    try:
        success = init_project(
            project_name=args.project_name,
            root=args.root,
            header_dir=args.header_dir,
            reset_git=args.reset_git,
            author=args.author,
            description=args.description,
        )
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nAborted.")
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
