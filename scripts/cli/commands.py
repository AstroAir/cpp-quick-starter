"""
CLI commands implementation - init, add, etc.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from .ui import (
    Spinner,
    ProgressBar,
    print_banner,
    print_box,
    print_list,
    print_step,
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
)
from . import prompts


# ============================================================================
# Project Configuration
# ============================================================================

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
    "docs/getting-started.md",
    ".github/workflows/ci.yml",
    ".github/workflows/code-quality.yml",
    ".github/workflows/release.yml",
    "src/main.cpp",
    "examples/example_01.cpp",
    "tests/unit/greeting_test.cpp",
    "tests/unit/string_utils_test.cpp",
    "tests/integration/smoke_test.cpp",
    "benchmarks/string_utils_bench.cpp",
]

# Template markers
OLD_PROJECT_NAME = "cpp_quick_starter"
OLD_PROJECT_NAME_KEBAB = "cpp-quick-starter"
OLD_PROJECT_NAME_PASCAL = "CppQuickStarter"
OLD_HEADER_DIR = "project_name"


# ============================================================================
# Name Conversion Utilities
# ============================================================================


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


def to_upper_snake(name: str) -> str:
    """Convert name to UPPER_SNAKE_CASE."""
    return to_snake_case(name).upper()


# ============================================================================
# File Operations
# ============================================================================


def replace_in_file(file_path: Path, replacements: Dict[str, str]) -> bool:
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
    except (UnicodeDecodeError, PermissionError):
        pass

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
                ).replace(f"#include <{old_dir}/", f"#include <{new_dir}/")

                if new_content != content:
                    file_path.write_text(new_content, encoding="utf-8")
                    count += 1
            except (UnicodeDecodeError, PermissionError):
                pass

    return count


# ============================================================================
# Init Command
# ============================================================================


def cmd_init(root: Optional[Path] = None, quick: bool = False) -> bool:
    """
    Interactive project initialization wizard.
    """
    print_banner(
        "C++ Quick Starter",
        "Modern C++20 Project Scaffolding",
        "1.0.0",
    )

    if root is None:
        root = Path(__file__).parent.parent.parent

    root = root.resolve()

    print_info(f"Project root: {cyan(str(root))}\n")

    # Step 1: Project name
    print_step(1, 5, "Project Information")

    project_name = prompts.project_name(
        "What is your project name?",
        default="my-awesome-lib",
    )

    # Generate name variants
    snake_name = to_snake_case(project_name)
    kebab_name = to_kebab_case(project_name)
    pascal_name = to_pascal_case(project_name)

    if not quick:
        print()
        print_box(
            [
                f"snake_case:  {cyan(snake_name)}",
                f"kebab-case:  {cyan(kebab_name)}",
                f"PascalCase:  {cyan(pascal_name)}",
                f"UPPER_SNAKE: {cyan(to_upper_snake(project_name))}",
            ],
            title="Generated Names",
        )

    # Step 2: Author and description
    print_step(2, 5, "Author Information")

    author = prompts.text(
        "Author name",
        default=get_git_user() or "Your Name",
        required=False,
    )

    description = prompts.text(
        "Project description",
        default="A modern C++ library",
        required=False,
    )

    # Step 3: Features
    print_step(3, 5, "Features")

    features = prompts.multiselect(
        "Select features to include",
        choices=[
            "Unit Tests (Google Test)",
            "Benchmarks (Google Benchmark)",
            "Examples",
            "Documentation (Doxygen + MkDocs)",
            "vcpkg Integration",
            "Conan Integration",
        ],
        defaults=[0, 2],  # Tests and Examples by default
    )

    feature_flags = {
        "tests": 0 in [f[0] for f in features],
        "benchmarks": 1 in [f[0] for f in features],
        "examples": 2 in [f[0] for f in features],
        "docs": 3 in [f[0] for f in features],
        "vcpkg": 4 in [f[0] for f in features],
        "conan": 5 in [f[0] for f in features],
    }

    # Step 4: Build system
    print_step(4, 5, "Build Configuration")

    _, build_system = prompts.select(
        "Primary build system",
        choices=["CMake", "xmake", "Both"],
        default=2,
        descriptions=[
            "Industry standard, wide IDE support",
            "Fast, Lua-based, modern",
            "Keep both build systems",
        ],
    )

    _, cpp_standard = prompts.select(
        "C++ standard",
        choices=["C++20", "C++23", "C++17"],
        default=0,
    )

    # Step 5: Git
    print_step(5, 5, "Version Control")

    reset_git = prompts.confirm(
        "Reset git history for a fresh start?",
        default=False,
    )

    # Summary
    print()
    print_box(
        [
            f"Project:     {cyan(project_name)}",
            f"Author:      {cyan(author)}",
            f"Description: {cyan(description)}",
            f"Build:       {cyan(build_system)}",
            f"Standard:    {cyan(cpp_standard)}",
            f"Git Reset:   {cyan('Yes' if reset_git else 'No')}",
        ],
        title="Configuration Summary",
    )
    print()

    if not prompts.confirm("Proceed with initialization?", default=True):
        print_warning("Initialization cancelled.")
        return False

    # Execute initialization
    print()
    return execute_init(
        root=root,
        project_name=project_name,
        author=author,
        description=description,
        feature_flags=feature_flags,
        build_system=build_system,
        cpp_standard=cpp_standard,
        reset_git=reset_git,
    )


def execute_init(
    root: Path,
    project_name: str,
    author: str,
    description: str,
    feature_flags: Dict[str, bool],
    build_system: str,
    cpp_standard: str,
    reset_git: bool,
) -> bool:
    """Execute the actual initialization."""

    snake_name = to_snake_case(project_name)
    kebab_name = to_kebab_case(project_name)
    pascal_name = to_pascal_case(project_name)
    header_name = snake_name

    # Build replacements
    replacements = {
        OLD_PROJECT_NAME: snake_name,
        OLD_PROJECT_NAME_KEBAB: kebab_name,
        OLD_PROJECT_NAME_PASCAL: pascal_name,
        OLD_HEADER_DIR: header_name,
        "CPP_QUICK_STARTER": to_upper_snake(project_name),
    }

    if author:
        replacements["Your Name"] = author
        replacements["AstroAir"] = author

    if description:
        replacements[
            "A modern C++20 project template with best practices for quick project bootstrapping."
        ] = description

    # Update C++ standard if not C++20
    if cpp_standard == "C++23":
        replacements["cxx_std_20"] = "cxx_std_23"
        replacements["cxx20"] = "cxx23"
        replacements["C++20"] = "C++23"
    elif cpp_standard == "C++17":
        replacements["cxx_std_20"] = "cxx_std_17"
        replacements["cxx20"] = "cxx17"
        replacements["C++20"] = "C++17"

    total_steps = 5
    current_step = 0

    # Step 1: Update files
    current_step += 1
    with Spinner(f"Updating project files...") as spinner:
        updated_count = 0
        for file_rel in FILES_TO_UPDATE:
            file_path = root / file_rel
            if replace_in_file(file_path, replacements):
                updated_count += 1
        spinner.succeed(f"Updated {updated_count} files")

    # Step 2: Update includes
    current_step += 1
    with Spinner("Updating #include directives...") as spinner:
        include_count = update_header_includes(root, OLD_HEADER_DIR, header_name)
        spinner.succeed(f"Updated {include_count} source files")

    # Step 3: Rename directories
    current_step += 1
    with Spinner("Renaming directories...") as spinner:
        old_dir = root / "include" / OLD_HEADER_DIR
        new_dir = root / "include" / header_name
        if old_dir.exists() and not new_dir.exists():
            old_dir.rename(new_dir)
            spinner.succeed(f"Renamed include/{OLD_HEADER_DIR} → include/{header_name}")
        else:
            spinner.info("No directories to rename")

    # Step 4: Create fresh CHANGELOG
    current_step += 1
    with Spinner("Creating fresh CHANGELOG...") as spinner:
        changelog = root / "CHANGELOG.md"
        changelog_content = f"""# Changelog

All notable changes to {project_name} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project setup from cpp-quick-starter template

"""
        changelog.write_text(changelog_content, encoding="utf-8")
        spinner.succeed("Created fresh CHANGELOG.md")

    # Step 5: Reset git
    current_step += 1
    if reset_git:
        with Spinner("Resetting git history...") as spinner:
            git_dir = root / ".git"
            if git_dir.exists():
                shutil.rmtree(git_dir)
            subprocess.run(
                ["git", "init"],
                cwd=root,
                capture_output=True,
            )
            spinner.succeed("Initialized fresh git repository")
    else:
        print_info("Keeping existing git history")

    # Remove unused build system files
    if build_system == "CMake":
        xmake_file = root / "xmake.lua"
        if xmake_file.exists():
            xmake_file.unlink()
            print_info("Removed xmake.lua (CMake-only mode)")
    elif build_system == "xmake":
        for f in ["CMakeLists.txt", "CMakePresets.json"]:
            cmake_file = root / f
            if cmake_file.exists():
                cmake_file.unlink()
        print_info("Removed CMake files (xmake-only mode)")

    # Remove unused feature files
    if not feature_flags.get("vcpkg"):
        vcpkg_file = root / "vcpkg.json"
        if vcpkg_file.exists():
            vcpkg_file.unlink()

    if not feature_flags.get("conan"):
        conan_file = root / "conanfile.txt"
        if conan_file.exists():
            conan_file.unlink()

    # Success!
    print()
    print_success(bold(f"Project '{project_name}' initialized successfully!"))
    print()

    print_box(
        [
            f"{green(Symbols.SUCCESS)} Build:   {dim('cmake --preset ninja-debug')}",
            f"{green(Symbols.SUCCESS)} Test:    {dim('ctest --preset ninja-debug')}",
            f"{green(Symbols.SUCCESS)} Format:  {dim('./scripts/format.sh')}",
        ],
        title="Next Steps",
    )

    print()
    print_list(
        [
            "Review and update README.md",
            "Update LICENSE with your information",
            "Start coding in src/ and include/",
        ]
    )
    print()

    return True


# ============================================================================
# Add Module Command
# ============================================================================


def cmd_add_module(root: Optional[Path] = None) -> bool:
    """
    Add a new module/component to the project.
    """
    print_banner(
        "Add Module",
        "Create a new module with header, source, and tests",
        "1.0.0",
    )

    if root is None:
        root = Path.cwd()

    root = root.resolve()

    # Detect project name from CMakeLists.txt
    project_info = detect_project_info(root)
    if not project_info:
        print_error("Could not detect project information. Are you in a cpp-quick-starter project?")
        return False

    project_name = project_info["name"]
    header_dir = project_info["header_dir"]

    print_info(f"Project: {cyan(project_name)}")
    print_info(f"Include dir: {cyan(f'include/{header_dir}/')}\n")

    # Get module info
    module_name = prompts.text(
        "Module name",
        placeholder="e.g., networking, math, utils",
        validate=lambda x: bool(re.match(r"^[a-z][a-z0-9_]*$", x)),
        validate_message="Module name must be lowercase, start with letter, and contain only letters, numbers, underscores",
    )

    _, module_type = prompts.select(
        "Module type",
        choices=["Class", "Header-only", "Functions"],
        descriptions=[
            "Class with .hpp and .cpp files",
            "Header-only template library",
            "Standalone utility functions",
        ],
    )

    class_name = ""
    if module_type == "Class":
        class_name = prompts.text(
            "Class name",
            default=to_pascal_case(module_name),
        )

    add_tests = prompts.confirm("Add unit tests?", default=True)

    # Create the module
    print()

    with Spinner(f"Creating module '{module_name}'...") as spinner:
        try:
            create_module(
                root=root,
                header_dir=header_dir,
                module_name=module_name,
                module_type=module_type,
                class_name=class_name,
                project_name=project_name,
                add_tests=add_tests,
            )
            spinner.succeed(f"Module '{module_name}' created successfully")
        except Exception as e:
            spinner.fail(f"Failed to create module: {e}")
            return False

    # Show created files
    print()
    print_box(
        [
            f"Header: {cyan(f'include/{header_dir}/{module_name}.hpp')}",
            f"Source: {cyan(f'src/{module_name}.cpp')}" if module_type != "Header-only" else "",
            f"Tests:  {cyan(f'tests/unit/test_{module_name}.cpp')}" if add_tests else "",
        ],
        title="Created Files",
    )

    print()
    print_warning("Don't forget to add the source file to CMakeLists.txt!")
    print()

    return True


def create_module(
    root: Path,
    header_dir: str,
    module_name: str,
    module_type: str,
    class_name: str,
    project_name: str,
    add_tests: bool,
) -> None:
    """Create module files."""
    snake_name = to_snake_case(project_name)
    upper_name = to_upper_snake(module_name)
    namespace = snake_name

    # Header
    header_path = root / "include" / header_dir / f"{module_name}.hpp"
    header_path.parent.mkdir(parents=True, exist_ok=True)

    if module_type == "Class":
        header_content = f"""#pragma once

namespace {namespace} {{

class {class_name} {{
public:
    {class_name}();
    ~{class_name}();

    // Copy
    {class_name}(const {class_name}&) = default;
    {class_name}& operator=(const {class_name}&) = default;

    // Move
    {class_name}({class_name}&&) noexcept = default;
    {class_name}& operator=({class_name}&&) noexcept = default;

private:
    // Add private members here
}};

}}  // namespace {namespace}
"""
    elif module_type == "Header-only":
        header_content = f"""#pragma once

namespace {namespace} {{

template <typename T>
class {class_name or to_pascal_case(module_name)} {{
public:
    // Add template implementation here
}};

}}  // namespace {namespace}
"""
    else:  # Functions
        header_content = f"""#pragma once

namespace {namespace} {{

// Add function declarations here

}}  // namespace {namespace}
"""

    header_path.write_text(header_content, encoding="utf-8")

    # Source (if not header-only)
    if module_type != "Header-only":
        src_path = root / "src" / f"{module_name}.cpp"
        src_path.parent.mkdir(parents=True, exist_ok=True)

        if module_type == "Class":
            src_content = f"""#include "{header_dir}/{module_name}.hpp"

namespace {namespace} {{

{class_name}::{class_name}() = default;

{class_name}::~{class_name}() = default;

}}  // namespace {namespace}
"""
        else:
            src_content = f"""#include "{header_dir}/{module_name}.hpp"

namespace {namespace} {{

// Add function implementations here

}}  // namespace {namespace}
"""

        src_path.write_text(src_content, encoding="utf-8")

    # Tests
    if add_tests:
        test_path = root / "tests" / "unit" / f"test_{module_name}.cpp"
        test_path.parent.mkdir(parents=True, exist_ok=True)

        test_content = f"""#include <gtest/gtest.h>
#include "{header_dir}/{module_name}.hpp"

namespace {namespace}::test {{

class {class_name or to_pascal_case(module_name)}Test : public ::testing::Test {{
protected:
    void SetUp() override {{
        // Setup code here
    }}

    void TearDown() override {{
        // Teardown code here
    }}
}};

TEST_F({class_name or to_pascal_case(module_name)}Test, BasicTest) {{
    // Add test code here
    EXPECT_TRUE(true);
}}

}}  // namespace {namespace}::test
"""

        test_path.write_text(test_content, encoding="utf-8")


# ============================================================================
# Add Dependency Command
# ============================================================================


def cmd_add_dependency(root: Optional[Path] = None) -> bool:
    """
    Add a dependency to the project.
    """
    print_banner(
        "Add Dependency",
        "Add a package dependency to your project",
        "1.0.0",
    )

    if root is None:
        root = Path.cwd()

    root = root.resolve()

    # Detect available package managers
    has_vcpkg = (root / "vcpkg.json").exists()
    has_conan = (root / "conanfile.txt").exists()

    if not has_vcpkg and not has_conan:
        print_error("No package manager configuration found.")
        print_info("Create vcpkg.json or conanfile.txt first.")
        return False

    pkg_managers = []
    if has_vcpkg:
        pkg_managers.append("vcpkg")
    if has_conan:
        pkg_managers.append("Conan")

    if len(pkg_managers) > 1:
        _, pkg_manager = prompts.select(
            "Which package manager?",
            choices=pkg_managers,
        )
    else:
        pkg_manager = pkg_managers[0]
        print_info(f"Using {cyan(pkg_manager)}")

    # Common packages
    common_packages = [
        ("fmt", "Modern formatting library"),
        ("spdlog", "Fast C++ logging library"),
        ("nlohmann-json", "JSON for Modern C++"),
        ("boost", "Boost C++ Libraries"),
        ("catch2", "Test framework"),
        ("cxxopts", "Command line parser"),
        ("Other", "Enter custom package name"),
    ]

    _, pkg_choice = prompts.select(
        "Select package",
        choices=[p[0] for p in common_packages],
        descriptions=[p[1] for p in common_packages],
    )

    if pkg_choice == "Other":
        package_name = prompts.text("Package name")
    else:
        package_name = pkg_choice

    # Add to configuration
    print()
    with Spinner(f"Adding {package_name} to {pkg_manager}...") as spinner:
        try:
            if pkg_manager == "vcpkg":
                add_vcpkg_dependency(root, package_name)
            else:
                add_conan_dependency(root, package_name)
            spinner.succeed(f"Added {package_name}")
        except Exception as e:
            spinner.fail(f"Failed: {e}")
            return False

    print()
    print_success(f"Added {cyan(package_name)} to {pkg_manager}")

    if pkg_manager == "vcpkg":
        print_info(f"Run: {dim('vcpkg install')}")
    else:
        print_info(f"Run: {dim('conan install . --output-folder=build --build=missing')}")

    return True


def add_vcpkg_dependency(root: Path, package: str) -> None:
    """Add a dependency to vcpkg.json."""
    import json

    vcpkg_path = root / "vcpkg.json"
    with open(vcpkg_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    if "dependencies" not in config:
        config["dependencies"] = []

    if package not in config["dependencies"]:
        config["dependencies"].append(package)

    with open(vcpkg_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def add_conan_dependency(root: Path, package: str, version: str = "") -> None:
    """Add a dependency to conanfile.txt."""
    conan_path = root / "conanfile.txt"
    content = conan_path.read_text(encoding="utf-8")

    # Find [requires] section and add package
    if "[requires]" in content:
        pkg_line = f"{package}/{version}" if version else package
        if pkg_line not in content and package not in content:
            content = content.replace("[requires]", f"[requires]\n{pkg_line}")
    else:
        pkg_line = f"{package}/{version}" if version else package
        content = f"[requires]\n{pkg_line}\n\n" + content

    conan_path.write_text(content, encoding="utf-8")


# ============================================================================
# Strip Language Command
# ============================================================================


def cmd_strip_language(root: Optional[Path] = None, lang: str = "zh") -> bool:
    """
    Strip a language from bilingual documentation files.
    
    Args:
        root: Project root directory
        lang: Language to remove ('en' or 'zh')
    """
    print_banner(
        "Strip Language",
        f"Remove {'Chinese' if lang == 'zh' else 'English'} content from docs",
        "1.0.0",
    )

    if root is None:
        root = Path.cwd()

    root = root.resolve()
    docs_dir = root / "docs"

    if not docs_dir.exists():
        print_error("docs/ directory not found.")
        return False

    # Find all markdown files
    md_files = list(docs_dir.rglob("*.md"))
    
    if not md_files:
        print_error("No markdown files found in docs/")
        return False

    print_info(f"Found {len(md_files)} markdown files")
    print()

    # Confirm
    lang_name = "Chinese (ZH)" if lang == "zh" else "English (EN)"
    if not prompts.confirm(f"Remove {lang_name} content from all docs?", default=False):
        print_warning("Cancelled.")
        return False

    print()
    
    # Process files
    processed = 0
    with Spinner(f"Stripping {lang_name} content...") as spinner:
        for md_file in md_files:
            if strip_language_from_file(md_file, lang):
                processed += 1
        spinner.succeed(f"Processed {processed} files")

    print()
    print_success(f"Removed {lang_name} content from documentation.")
    
    return True


def strip_language_from_file(file_path: Path, lang: str) -> bool:
    """
    Remove language-specific content from a markdown file.
    
    Removes content between <!-- [EN] --> and <!-- [/EN] --> markers (for lang='en')
    or <!-- [ZH] --> and <!-- [/ZH] --> markers (for lang='zh').
    Also cleans up bilingual headers like "Title / 标题" to single language.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        original = content

        # Remove language blocks
        if lang == "en":
            # Remove English blocks
            content = re.sub(
                r'<!-- \[EN\] -->\s*\n?(.*?)\n?<!-- \[/EN\] -->\s*\n?',
                '',
                content,
                flags=re.DOTALL
            )
            # Clean ZH markers but keep content
            content = re.sub(r'<!-- \[ZH\] -->\s*\n?', '', content)
            content = re.sub(r'<!-- \[/ZH\] -->\s*\n?', '', content)
            # Clean bilingual headers: "English / 中文" -> "中文"
            content = re.sub(r'^(#+\s*)([^/\n]+)\s*/\s*(.+)$', r'\1\3', content, flags=re.MULTILINE)
            # Clean inline bilingual: "word / 词" -> "词"
            content = re.sub(r'([A-Za-z][A-Za-z\s]+)\s*/\s*([\u4e00-\u9fff]+)', r'\2', content)
        else:  # lang == "zh"
            # Remove Chinese blocks
            content = re.sub(
                r'<!-- \[ZH\] -->\s*\n?(.*?)\n?<!-- \[/ZH\] -->\s*\n?',
                '',
                content,
                flags=re.DOTALL
            )
            # Clean EN markers but keep content
            content = re.sub(r'<!-- \[EN\] -->\s*\n?', '', content)
            content = re.sub(r'<!-- \[/EN\] -->\s*\n?', '', content)
            # Clean bilingual headers: "English / 中文" -> "English"
            content = re.sub(r'^(#+\s*)([^/\n]+)\s*/\s*(.+)$', r'\1\2', content, flags=re.MULTILINE)
            # Clean inline bilingual: "word / 词" -> "word"
            content = re.sub(r'([A-Za-z][A-Za-z\s]+)\s*/\s*([\u4e00-\u9fff]+)', r'\1', content)

        # Clean up multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        if content != original:
            file_path.write_text(content, encoding="utf-8")
            return True
            
    except (UnicodeDecodeError, PermissionError) as e:
        pass
    
    return False


# ============================================================================
# Utilities
# ============================================================================


def get_git_user() -> Optional[str]:
    """Get git user name."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def detect_project_info(root: Path) -> Optional[Dict[str, str]]:
    """Detect project information from CMakeLists.txt."""
    cmake_file = root / "CMakeLists.txt"
    if not cmake_file.exists():
        return None

    content = cmake_file.read_text(encoding="utf-8")

    # Find project name
    match = re.search(r"project\s*\(\s*(\w+)", content)
    if not match:
        return None

    project_name = match.group(1)

    # Find header directory
    header_dir = to_snake_case(project_name)
    include_dir = root / "include"
    if include_dir.exists():
        for d in include_dir.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                header_dir = d.name
                break

    return {
        "name": project_name,
        "header_dir": header_dir,
    }
