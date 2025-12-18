# cpp-quick-starter

[![CI](https://github.com/AstroAir/cpp-quick-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/AstroAir/cpp-quick-starter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++20](https://img.shields.io/badge/C%2B%2B-20-blue.svg)](https://isocpp.org/std/the-standard)
[![Template](https://img.shields.io/badge/Template-Repository-green.svg)](https://github.com/AstroAir/cpp-quick-starter/generate)

[English](README.md) | [中文](README_CN.md)

现代化的 C++20 项目模板，集成最佳实践，助您快速启动新项目。

## ✨ 特性

- **现代 C++20** - 使用最新 C++ 标准特性
- **多构建系统** - 支持 CMake、xmake
- **包管理器** - 集成 vcpkg、Conan
- **跨平台支持** - Windows、Linux、macOS，提供平台专属预设
- **脚手架工具** - 项目初始化脚本，轻松自定义
- **测试框架** - Google Test 单元测试和集成测试
- **性能基准** - Google Benchmark 支持
- **代码质量** - clang-format、clang-tidy、cppcheck
- **CI/CD** - GitHub Actions 工作流
- **文档生成** - Doxygen + MkDocs

## 🚀 使用此模板

### 方式一：GitHub 模板（推荐）

点击 GitHub 上的 **"Use this template"** 按钮，或使用命令行：

```bash
gh repo create my-project --template AstroAir/cpp-quick-starter
```

### 方式二：克隆并初始化

```bash
git clone https://github.com/AstroAir/cpp-quick-starter.git my-project
cd my-project
python scripts/init-project.py "MyProject" --reset-git
```

### 初始化您的项目

```bash
# 基础初始化
python scripts/init-project.py "MyAwesomeLib"

# 使用全部选项
python scripts/init-project.py "MyAwesomeLib" \
    --author "您的名字" \
    --description "我的 C++ 库" \
    --reset-git
```

脚本会自动重命名所有项目引用，为您设置全新的项目。

## 📁 项目结构

```text
cpp-quick-starter/
├── .github/                    # GitHub 配置
│   ├── ISSUE_TEMPLATE/         # Issue 模板
│   └── workflows/              # CI/CD 工作流
├── benchmarks/                 # 基准测试
├── cmake/                      # CMake 模块
│   ├── CompilerWarnings.cmake
│   ├── Conan.cmake
│   ├── Doxygen.cmake
│   ├── Sanitizers.cmake
│   └── StaticAnalyzers.cmake
├── docs/                       # 文档
│   ├── api/
│   └── guides/
├── examples/                   # 示例代码
├── include/                    # 公共头文件
│   └── project_name/
│       ├── core/
│       │   └── greeting.hpp
│       └── utils/
│           └── string_utils.hpp
├── scripts/                    # 工具脚本
├── src/                        # 源文件
│   ├── core/
│   │   └── greeting.cpp
│   ├── utils/
│   │   └── string_utils.cpp
│   └── main.cpp
├── tests/                      # 测试文件
│   ├── integration/
│   └── unit/
├── .clang-format               # 代码格式化规则
├── .clang-tidy                 # 静态分析规则
├── .clangd                     # Clangd 配置
├── CMakeLists.txt              # CMake 构建配置
├── CMakePresets.json           # CMake 预设
├── conanfile.txt               # Conan 依赖
├── vcpkg.json                  # vcpkg 依赖
└── xmake.lua                   # xmake 构建配置
```

## 🚀 快速开始

### 环境要求

- 支持 C++20 的编译器 (GCC 10+, Clang 10+, MSVC 2019+)
- CMake 3.21+ 或 xmake
- (可选) vcpkg 或 Conan 包管理器

### 检查开发环境

```bash
# Unix (Linux/macOS)
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1
```

### 使用脚本构建（跨平台）

```bash
# Unix
./scripts/build.sh                    # 默认预设
./scripts/build.sh ninja-release      # 发布构建
./scripts/build.sh --clean            # 清理后构建

# Windows PowerShell
.\scripts\build.ps1
.\scripts\build.ps1 -Preset ninja-release
.\scripts\build.ps1 -Clean
```

### 使用 CMake 预设构建

```bash
# 配置并构建
cmake --preset ninja-debug
cmake --build --preset ninja-debug

# 运行测试
ctest --preset ninja-debug

# 或使用工作流预设 (CMake 3.25+)
cmake --workflow --preset dev      # 配置 + 构建 + 测试
cmake --workflow --preset ci       # 警告视为错误
cmake --workflow --preset release  # 发布构建
```

### 使用 xmake 构建

```bash
xmake                              # 配置并构建
xmake run cpp_quick_starter_app    # 运行应用程序
xmake run unit_tests               # 运行测试
```

### CMake 预设

| 预设 | 描述 | 平台 |
|------|------|------|
| `ninja-debug` | Ninja 调试构建 | 全平台 |
| `ninja-release` | Ninja 发布构建 | 全平台 |
| `ninja-ci` | CI 构建（警告视为错误） | 全平台 |
| `ninja-sanitize` | 带内存检测的调试构建 | Unix |
| `vs-debug` | Visual Studio 调试 | Windows |
| `vs-release` | Visual Studio 发布 | Windows |
| `macos-debug` | macOS 调试 | macOS |
| `linux-debug` | Linux 调试 | Linux |
| `linux-clang-debug` | Linux Clang 调试 | Linux |
| `vcpkg-debug` | 使用 vcpkg 工具链 | 全平台 |

### CMake 选项

| 选项 | 默认值 | 描述 |
|------|--------|------|
| `CPP_QUICK_STARTER_ENABLE_WARNINGS` | ON | 启用编译器警告 |
| `CPP_QUICK_STARTER_WARNINGS_AS_ERRORS` | OFF | 将警告视为错误 |
| `CPP_QUICK_STARTER_ENABLE_SANITIZERS` | OFF | 启用内存检测工具 |
| `CPP_QUICK_STARTER_ENABLE_CLANG_TIDY` | OFF | 启用 clang-tidy |
| `CPP_QUICK_STARTER_ENABLE_CPPCHECK` | OFF | 启用 cppcheck |
| `CPP_QUICK_STARTER_BUILD_TESTS` | ON | 构建测试 |
| `CPP_QUICK_STARTER_BUILD_BENCHMARKS` | OFF | 构建基准测试 |
| `CPP_QUICK_STARTER_BUILD_EXAMPLES` | ON | 构建示例 |
| `CPP_QUICK_STARTER_BUILD_DOCS` | OFF | 构建文档 |

## 📦 包管理

### vcpkg

```bash
# 安装依赖
vcpkg install

# 使用 vcpkg 工具链配置
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Conan

```bash
# 安装依赖
conan install . --output-folder=build --build=missing

# 使用 Conan 工具链配置
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```

## 🧪 测试

```bash
# 使用 CTest 运行所有测试
ctest --test-dir build --output-on-failure

# 或直接运行测试可执行文件
./build/tests/unit_tests
./build/tests/integration_tests
```

## 📊 基准测试

```bash
# 启用基准测试
cmake -B build -S . -DCPP_QUICK_STARTER_BUILD_BENCHMARKS=ON
cmake --build build

# 运行基准测试
./build/benchmarks/benchmarks
```

## 🛠️ CLI 脚手架工具

美观的交互式 CLI 工具（灵感来自 npm/yarn）：

```bash
# 交互式项目初始化
python scripts/cqs.py init

# 添加新模块
python scripts/cqs.py add module

# 添加依赖
python scripts/cqs.py add dep

# 检查开发环境
python scripts/cqs.py doctor

# 显示项目信息
python scripts/cqs.py info
```

### 构建系统集成

所有 CLI 工具已集成到 CMake 和 xmake：

```bash
# CMake 目标
cmake --build build --target format       # 格式化代码
cmake --build build --target format-check # 检查格式
cmake --build build --target doctor       # 检查环境
cmake --build build --target add-module   # 添加模块（交互式）
cmake --build build --target add-dep      # 添加依赖（交互式）

# xmake 任务
xmake format           # 格式化代码
xmake format -c        # 检查格式
xmake doctor           # 检查环境
xmake add-module       # 添加模块（交互式）
xmake add-dep          # 添加依赖（交互式）
xmake tasks            # 列出所有任务
```

### CLI 命令

| 命令 | CMake 目标 | xmake 任务 |
|------|------------|------------|
| `cqs init` | - | `xmake init` |
| `cqs add module` | `add-module` | `xmake add-module` |
| `cqs add dep` | `add-dep` | `xmake add-dep` |
| `cqs doctor` | `doctor` | `xmake doctor` |
| `cqs info` | `info` | `xmake info` |
| 格式化代码 | `format` | `xmake format` |
| 检查格式 | `format-check` | `xmake format -c` |

## 📜 工具脚本

跨平台脚本支持常见开发任务：

| 脚本 | Unix | Windows | 描述 |
|------|------|---------|------|
| 环境检查 | `./scripts/setup.sh` | `.\scripts\setup.ps1` | 检查开发环境 |
| 构建 | `./scripts/build.sh` | `.\scripts\build.ps1` | 配置并构建项目 |
| 测试 | `./scripts/test.sh` | `.\scripts\test.ps1` | 运行测试 |
| 格式化 | `./scripts/format.sh` | `.\scripts\format.ps1` | 使用 clang-format 格式化代码 |
| 清理 | `./scripts/clean.sh` | `.\scripts\clean.ps1` | 清理构建产物 |
| 初始化 | `python scripts/init-project.py` | `python scripts\init-project.py` | 初始化新项目（非交互式） |

## 🔍 代码质量

### 代码格式化

```bash
# Unix
./scripts/format.sh              # 格式化所有文件
./scripts/format.sh --check      # 仅检查不修改（CI 模式）

# Windows
.\scripts\format.ps1
.\scripts\format.ps1 -Check
```

### 静态分析

```bash
# 启用 clang-tidy
cmake -B build -S . -DCPP_QUICK_STARTER_ENABLE_CLANG_TIDY=ON

# 启用 cppcheck
cmake -B build -S . -DCPP_QUICK_STARTER_ENABLE_CPPCHECK=ON

# 使用内存检测工具
cmake --preset ninja-sanitize
cmake --build --preset ninja-sanitize
```

## 📚 文档

```bash
# 构建文档
cmake -B build -S . -DCPP_QUICK_STARTER_BUILD_DOCS=ON
cmake --build build --target docs

# 本地预览 MkDocs
mkdocs serve
```

## 🤝 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Google Test](https://github.com/google/googletest)
- [Google Benchmark](https://github.com/google/benchmark)
- [CMake](https://cmake.org/)
- [xmake](https://xmake.io/)
