# Quick Start / 快速入门

<!-- [EN] -->
This guide helps you quickly get started with the cpp-quick-starter template.
<!-- [/EN] -->

<!-- [ZH] -->
本指南帮助您快速开始使用 cpp-quick-starter 模板。
<!-- [/ZH] -->

## Requirements / 环境要求

### Required Tools / 必需工具

- **C++20 compatible compiler / C++20 兼容编译器**：
  - GCC 10+ (Linux)
  - Clang 10+ (Linux/macOS)
  - MSVC 2019+ (Windows)
  - Apple Clang 13+ (macOS)
- **CMake 3.21+** or/或 **xmake**
- **Git**
- **Python 3** (for CLI tools / 用于 CLI 工具)

### Optional Tools / 可选工具

- **Ninja** - Fast build tool (recommended) / 快速构建工具（推荐）
- **vcpkg** or/或 **Conan** - Package manager / 包管理器
- **clang-format** - Code formatting / 代码格式化
- **clang-tidy** - Static analysis / 静态分析

### Check Environment / 检查环境

```bash
# Use CLI tool / 使用 CLI 工具检查
python scripts/cqs.py doctor

# Or use scripts / 或使用脚本
./scripts/setup.sh      # Unix
.\scripts\setup.ps1     # Windows
```

## Build with CMake / 使用 CMake 构建

```bash
# Configure and build with presets / 使用预设配置和构建
cmake --preset ninja-debug
cmake --build --preset ninja-debug

# Run tests / 运行测试
ctest --preset ninja-debug

# Workflow preset (CMake 3.25+) / 工作流预设
cmake --workflow --preset dev
```

## Build with xmake / 使用 xmake 构建

```bash
# Configure and build / 配置并构建
xmake f -m debug
xmake

# Run application / 运行应用程序
xmake run cpp_quick_starter_app

# Run tests / 运行测试
xmake run unit_tests
```

## Build with Scripts / 使用脚本构建

```bash
# Unix
./scripts/build.sh                    # Default / 默认构建
./scripts/build.sh ninja-release      # Release build / 发布构建
./scripts/build.sh --clean            # Clean build / 清理后构建

# Windows PowerShell
.\scripts\build.ps1
.\scripts\build.ps1 -Preset ninja-release
.\scripts\build.ps1 -Clean
```

## Next Steps / 下一步

<!-- [EN] -->
- See [CMake Guide](cmake.md) for all build options
- See [xmake Guide](xmake.md) for xmake usage
- See [Testing Guide](testing.md) for writing and running tests
- See [Code Quality](code-quality.md) for formatting and static analysis
<!-- [/EN] -->

<!-- [ZH] -->
- 查看 [CMake 指南](cmake.md) 了解所有构建选项
- 查看 [xmake 指南](xmake.md) 了解 xmake 使用方法
- 查看 [测试指南](testing.md) 编写和运行测试
- 查看 [代码质量](code-quality.md) 配置格式化和静态分析
<!-- [/ZH] -->
