# Scaffolding Guide / 脚手架指南

<!-- [EN] -->
This document describes the scaffolding tools and scripts available in cpp-quick-starter.
<!-- [/EN] -->

<!-- [ZH] -->
本文档描述 cpp-quick-starter 中可用的脚手架工具和脚本。
<!-- [/ZH] -->

## CLI Tool (cqs) / CLI 工具

<!-- [EN] -->
The `cqs` CLI provides a beautiful, interactive experience for project scaffolding, inspired by npm/yarn.
<!-- [/EN] -->

<!-- [ZH] -->
`cqs` CLI 提供美观的交互式项目脚手架体验，灵感来自 npm/yarn。
<!-- [/ZH] -->

### Quick Start / 快速开始

```bash
# Interactive project initialization / 交互式项目初始化
python scripts/cqs.py init

# Or on Unix with the wrapper script / 或在 Unix 上使用包装脚本
./scripts/cqs init

# On Windows / Windows 上
scripts\cqs.cmd init
```

### Available Commands / 可用命令

<!-- [EN] -->
| Command | Description |
|---------|-------------|
| `cqs init` | Initialize a new project interactively |
| `cqs add module` | Add a new module/component |
| `cqs add dep` | Add a package dependency |
| `cqs strip en` | Remove English from bilingual docs |
| `cqs strip zh` | Remove Chinese from bilingual docs |
| `cqs info` | Show project information |
| `cqs doctor` | Check development environment |
| `cqs help` | Show help message |
<!-- [/EN] -->

<!-- [ZH] -->
| 命令 | 描述 |
|------|------|
| `cqs init` | 交互式初始化新项目 |
| `cqs add module` | 添加新模块/组件 |
| `cqs add dep` | 添加包依赖 |
| `cqs strip en` | 从双语文档中移除英文 |
| `cqs strip zh` | 从双语文档中移除中文 |
| `cqs info` | 显示项目信息 |
| `cqs doctor` | 检查开发环境 |
| `cqs help` | 显示帮助信息 |
<!-- [/ZH] -->

## Project Initialization / 项目初始化

### Interactive Mode (Recommended) / 交互模式（推荐）

```bash
python scripts/cqs.py init
```

<!-- [EN] -->
The interactive wizard guides you through:

1. **Project name** - With automatic case conversion preview
2. **Author information** - Auto-detected from git config
3. **Features selection** - Tests, benchmarks, docs, package managers
4. **Build system** - CMake, xmake, or both
5. **C++ standard** - C++17, C++20, or C++23
6. **Git options** - Reset history for fresh start
<!-- [/EN] -->

<!-- [ZH] -->
交互向导将引导您完成：

1. **项目名称** - 自动预览名称转换
2. **作者信息** - 自动从 git config 检测
3. **功能选择** - 测试、基准测试、文档、包管理器
4. **构建系统** - CMake、xmake 或两者
5. **C++ 标准** - C++17、C++20 或 C++23
6. **Git 选项** - 重置历史以获得全新开始
<!-- [/ZH] -->

### Non-Interactive Mode / 非交互模式

<!-- [EN] -->
For CI/CD or scripting, use the legacy script:
<!-- [/EN] -->

<!-- [ZH] -->
用于 CI/CD 或脚本，使用传统脚本：
<!-- [/ZH] -->

```bash
python scripts/init-project.py PROJECT_NAME [OPTIONS]
```

#### Options / 选项

<!-- [EN] -->
| Option | Description |
|--------|-------------|
| `PROJECT_NAME` | Name for your project |
| `--header-dir NAME` | Custom name for include directory |
| `--author NAME` | Author name to use in files |
| `--description TEXT` | Project description |
| `--reset-git` | Reset git history for fresh start |
| `--root PATH` | Project root directory |
<!-- [/EN] -->

<!-- [ZH] -->
| 选项 | 描述 |
|------|------|
| `PROJECT_NAME` | 项目名称 |
| `--header-dir NAME` | 自定义 include 目录名称 |
| `--author NAME` | 使用的作者名称 |
| `--description TEXT` | 项目描述 |
| `--reset-git` | 重置 git 历史 |
| `--root PATH` | 项目根目录 |
<!-- [/ZH] -->

#### Examples / 示例

```bash
# Basic usage / 基本用法
python scripts/init-project.py MyAwesomeLib

# With all options / 使用所有选项
python scripts/init-project.py "My Awesome Library" \
    --header-dir myawesomelib \
    --author "John Doe" \
    --description "A fantastic C++ library" \
    --reset-git
```

#### What It Does / 功能说明

<!-- [EN] -->
1. **Name Conversion**: Converts your project name to multiple formats:
    - `snake_case` for C++ identifiers
    - `kebab-case` for file names and URLs
    - `PascalCase` for class names
    - `UPPER_SNAKE` for macros

2. **File Updates**: Updates project references in all configuration files

3. **Directory Renaming**: Renames `include/project_name/` to your project name

4. **Include Updates**: Updates all `#include` directives

5. **Fresh Start**: Creates new CHANGELOG.md and optionally resets git
<!-- [/EN] -->

<!-- [ZH] -->
1. **名称转换**：将项目名称转换为多种格式：
    - `snake_case` 用于 C++ 标识符
    - `kebab-case` 用于文件名和 URL
    - `PascalCase` 用于类名
    - `UPPER_SNAKE` 用于宏

2. **文件更新**：更新所有配置文件中的项目引用

3. **目录重命名**：将 `include/project_name/` 重命名为您的项目名称

4. **Include 更新**：更新所有 `#include` 指令

5. **全新开始**：创建新的 CHANGELOG.md 并可选重置 git
<!-- [/ZH] -->

## Build Scripts / 构建脚本

<!-- [EN] -->
Both Bash (Unix) and PowerShell (Windows) versions are available.
<!-- [/EN] -->

<!-- [ZH] -->
提供 Bash (Unix) 和 PowerShell (Windows) 两个版本。
<!-- [/ZH] -->

### build.sh / build.ps1

```bash
# Unix
./scripts/build.sh [PRESET] [OPTIONS]

# Windows
.\scripts\build.ps1 [-Preset NAME] [-Clean] [-Target NAME]
```

### test.sh / test.ps1

```bash
# Unix
./scripts/test.sh [--filter PATTERN] [--verbose] [--build]

# Windows
.\scripts\test.ps1 [-Filter PATTERN] [-Verbose] [-Build]
```

### format.sh / format.ps1

```bash
# Unix
./scripts/format.sh [--check]

# Windows
.\scripts\format.ps1 [-Check]
```

### clean.sh / clean.ps1

```bash
# Unix
./scripts/clean.sh [--all]

# Windows
.\scripts\clean.ps1 [-All]
```

### setup.sh / setup.ps1

<!-- [EN] -->
Checks your development environment for required and optional tools.
<!-- [/EN] -->

<!-- [ZH] -->
检查开发环境中的必需和可选工具。
<!-- [/ZH] -->

```bash
./scripts/setup.sh      # Unix
.\scripts\setup.ps1     # Windows
```

## CMake Workflow Presets / CMake 工作流预设

<!-- [EN] -->
CMake 3.25+ supports workflow presets for common development tasks:
<!-- [/EN] -->

<!-- [ZH] -->
CMake 3.25+ 支持工作流预设用于常见开发任务：
<!-- [/ZH] -->

```bash
# Development: configure + build + test / 开发：配置 + 构建 + 测试
cmake --workflow --preset dev

# CI: build with warnings as errors / CI：警告视为错误
cmake --workflow --preset ci

# Release: configure + build release / 发布：配置 + 构建发布版
cmake --workflow --preset release
```

## Adding New Features / 添加新功能

### Adding a New Source File / 添加新源文件

<!-- [EN] -->
1. Create header in `include/project_name/module/`
2. Create source in `src/module/`
3. Add to CMakeLists.txt
4. Add tests in `tests/unit/`
<!-- [/EN] -->

<!-- [ZH] -->
1. 在 `include/project_name/module/` 创建头文件
2. 在 `src/module/` 创建源文件
3. 添加到 CMakeLists.txt
4. 在 `tests/unit/` 添加测试
<!-- [/ZH] -->

```cpp
// include/project_name/module/feature.hpp
#pragma once
namespace project_name::module {
    class Feature { /* ... */ };
}

// src/module/feature.cpp
#include "project_name/module/feature.hpp"
namespace project_name::module {
    // Implementation
}
```

### Adding a Dependency / 添加依赖

#### Using CLI (Recommended) / 使用 CLI（推荐）

```bash
python scripts/cqs.py add dep
```

<!-- [EN] -->
The CLI will:

1. Detect available package managers (vcpkg/Conan)
2. Let you select from common packages or enter custom name
3. Automatically update configuration files
<!-- [/EN] -->

<!-- [ZH] -->
CLI 将会：

1. 检测可用的包管理器 (vcpkg/Conan)
2. 让您从常用包中选择或输入自定义名称
3. 自动更新配置文件
<!-- [/ZH] -->

#### Using vcpkg / 使用 vcpkg

```json
// vcpkg.json
{ "dependencies": ["fmt", "spdlog"] }
```

```bash
cmake --preset vcpkg-debug
```

#### Using Conan / 使用 Conan

```bash
conan install . --output-folder=build --build=missing
cmake -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```

## Add Module Command / 添加模块命令

```bash
python scripts/cqs.py add module
```

<!-- [EN] -->
Features:

- **Class module** - Creates .hpp and .cpp with class skeleton
- **Header-only** - Creates template header for header-only libraries
- **Functions** - Creates utility function module
- **Auto-generates tests** - Optional unit test file
<!-- [/EN] -->

<!-- [ZH] -->
功能：

- **类模块** - 创建带类骨架的 .hpp 和 .cpp
- **仅头文件** - 创建用于仅头文件库的模板头文件
- **函数** - 创建工具函数模块
- **自动生成测试** - 可选的单元测试文件
<!-- [/ZH] -->

## Environment Check / 环境检查

```bash
python scripts/cqs.py doctor

# Or via build system / 或通过构建系统
cmake --build build --target doctor
xmake doctor
```

<!-- [EN] -->
This checks for:

- **Required**: CMake, Git, Python
- **Compilers**: GCC, Clang, MSVC
- **Build tools**: Ninja, Make, xmake
- **Package managers**: vcpkg, Conan
- **Code quality**: clang-format, clang-tidy, cppcheck
- **Documentation**: Doxygen, MkDocs
<!-- [/EN] -->

<!-- [ZH] -->
检查以下工具：

- **必需**: CMake, Git, Python
- **编译器**: GCC, Clang, MSVC
- **构建工具**: Ninja, Make, xmake
- **包管理器**: vcpkg, Conan
- **代码质量**: clang-format, clang-tidy, cppcheck
- **文档**: Doxygen, MkDocs
<!-- [/ZH] -->

## Project Information / 项目信息

```bash
python scripts/cqs.py info

# Or via build system / 或通过构建系统
cmake --build build --target info
xmake info
```

## Build System Integration / 构建系统集成

<!-- [EN] -->
All CLI functionality is integrated into CMake and xmake for convenience.
<!-- [/EN] -->

<!-- [ZH] -->
所有 CLI 功能都已集成到 CMake 和 xmake 中，方便使用。
<!-- [/ZH] -->

### CMake Targets / CMake 目标

```bash
cmake --build build --target format        # Format code / 格式化代码
cmake --build build --target format-check  # Check format / 检查格式
cmake --build build --target doctor        # Check environment / 检查环境
cmake --build build --target add-module    # Add module / 添加模块
cmake --build build --target add-dep       # Add dependency / 添加依赖
```

### xmake Tasks / xmake 任务

```bash
xmake format               # Format code / 格式化代码
xmake format -c            # Check format / 检查格式
xmake doctor               # Check environment / 检查环境
xmake add-module           # Add module / 添加模块
xmake add-dep              # Add dependency / 添加依赖
xmake init                 # Initialize project / 初始化项目
xmake tasks                # List all tasks / 列出所有任务
```

### Quick Reference / 快速参考

<!-- [EN] -->
| Task | CMake | xmake | Python CLI |
|------|-------|-------|------------|
| Format code | `--target format` | `xmake format` | `cqs.py format` |
| Check format | `--target format-check` | `xmake format -c` | `cqs.py format --check` |
| Check env | `--target doctor` | `xmake doctor` | `cqs.py doctor` |
| Add module | `--target add-module` | `xmake add-module` | `cqs.py add module` |
| Add dep | `--target add-dep` | `xmake add-dep` | `cqs.py add dep` |
| Strip English | N/A | N/A | `cqs.py strip en` |
| Strip Chinese | N/A | N/A | `cqs.py strip zh` |
<!-- [/EN] -->

<!-- [ZH] -->
| 任务 | CMake | xmake | Python CLI |
|------|-------|-------|------------|
| 格式化代码 | `--target format` | `xmake format` | `cqs.py format` |
| 检查格式 | `--target format-check` | `xmake format -c` | `cqs.py format --check` |
| 检查环境 | `--target doctor` | `xmake doctor` | `cqs.py doctor` |
| 添加模块 | `--target add-module` | `xmake add-module` | `cqs.py add module` |
| 添加依赖 | `--target add-dep` | `xmake add-dep` | `cqs.py add dep` |
| 移除英文 | N/A | N/A | `cqs.py strip en` |
| 移除中文 | N/A | N/A | `cqs.py strip zh` |
<!-- [/ZH] -->
