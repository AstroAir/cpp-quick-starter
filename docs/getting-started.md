# Getting Started / 快速入门

<!-- [EN] -->
This guide will help you get started with the cpp-quick-starter template.
<!-- [/EN] -->

<!-- [ZH] -->
本指南帮助您快速开始使用 cpp-quick-starter 模板。
<!-- [/ZH] -->

## Prerequisites / 环境要求

### Required Tools / 必需工具

- **C++20 compatible compiler / C++20 兼容编译器**:
  - GCC 10+ (Linux)
  - Clang 10+ (Linux/macOS)
  - MSVC 2019+ (Windows)
  - Apple Clang 13+ (macOS)
- **CMake 3.21+** or/或 **xmake**
- **Git**
- **Python 3** (for CLI tools / 用于 CLI 工具)

### Optional Tools / 可选工具

- **Ninja** - Fast build system (recommended) / 快速构建工具（推荐）
- **vcpkg** or **Conan** - Package management / 包管理器
- **clang-format** - Code formatting / 代码格式化
- **clang-tidy** - Static analysis / 静态分析
- **Doxygen** - API documentation / API 文档
- **MkDocs** - Project documentation / 项目文档

### Checking Your Environment / 检查环境

<!-- [EN] -->
Run the setup script to check your environment:
<!-- [/EN] -->

<!-- [ZH] -->
运行设置脚本检查您的环境：
<!-- [/ZH] -->

```bash
# Unix (Linux/macOS)
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1

# Or use CLI tool / 或使用 CLI 工具
python scripts/cqs.py doctor
```

## Installation / 安装

### From GitHub Template / 使用 GitHub 模板

<!-- [EN] -->
1. Click **"Use this template"** on the GitHub repository page
2. Create your new repository
3. Clone and initialize:
<!-- [/EN] -->

<!-- [ZH] -->
1. 点击 GitHub 仓库页面上的 **"Use this template"** 按钮
2. 创建您的新仓库
3. 克隆并初始化：
<!-- [/ZH] -->

```bash
git clone https://github.com/YOUR_USERNAME/your-project.git
cd your-project
python scripts/cqs.py init
```

### Manual Clone / 手动克隆

```bash
git clone https://github.com/AstroAir/cpp-quick-starter.git my-project
cd my-project
python scripts/cqs.py init
# Or non-interactive / 或非交互式
python scripts/init-project.py "MyProject" --reset-git
```

## Building / 构建

### Using CMake Presets (Recommended) / 使用 CMake 预设（推荐）

```bash
# List available presets / 列出可用预设
cmake --list-presets

# Configure and build / 配置并构建
cmake --preset ninja-debug
cmake --build --preset ninja-debug

# Run tests / 运行测试
ctest --preset ninja-debug

# Workflow preset (CMake 3.25+) / 工作流预设
cmake --workflow --preset dev
```

### Using Build Scripts / 使用构建脚本

```bash
# Unix
./scripts/build.sh                    # Default / 默认
./scripts/build.sh ninja-release      # Release build / 发布构建
./scripts/build.sh --clean            # Clean build / 清理后构建

# Windows PowerShell
.\scripts\build.ps1
.\scripts\build.ps1 -Preset ninja-release
.\scripts\build.ps1 -Clean
```

### Using xmake / 使用 xmake

```bash
xmake                              # Configure and build / 配置并构建
xmake run cpp_quick_starter_app    # Run application / 运行应用
xmake run unit_tests               # Run tests / 运行测试
```

## Project Structure / 项目结构

```
cpp-quick-starter/
├── include/project_name/     # Public headers / 公共头文件
│   ├── core/                 # Core functionality / 核心功能
│   └── utils/                # Utility functions / 工具函数
├── src/                      # Source files / 源文件
│   ├── core/                 # Core implementation / 核心实现
│   ├── utils/                # Utility implementation / 工具实现
│   └── main.cpp              # Application entry / 应用入口
├── tests/                    # Tests / 测试
│   ├── unit/                 # Unit tests / 单元测试
│   └── integration/          # Integration tests / 集成测试
├── benchmarks/               # Performance benchmarks / 性能基准
├── examples/                 # Example code / 示例代码
├── docs/                     # Documentation / 文档
├── scripts/                  # Build and utility scripts / 构建和工具脚本
├── cmake/                    # CMake modules / CMake 模块
├── .github/                  # GitHub configuration / GitHub 配置
├── CMakeLists.txt            # CMake configuration / CMake 配置
├── CMakePresets.json         # CMake presets / CMake 预设
├── xmake.lua                 # xmake configuration / xmake 配置
├── vcpkg.json                # vcpkg dependencies / vcpkg 依赖
└── conanfile.txt             # Conan dependencies / Conan 依赖
```

## CMake Options / CMake 选项

<!-- [EN] -->
| Option | Default | Description |
|--------|---------|-------------|
| `CPP_QUICK_STARTER_ENABLE_WARNINGS` | ON | Enable compiler warnings |
| `CPP_QUICK_STARTER_WARNINGS_AS_ERRORS` | OFF | Treat warnings as errors |
| `CPP_QUICK_STARTER_ENABLE_SANITIZERS` | OFF | Enable sanitizers |
| `CPP_QUICK_STARTER_ENABLE_CLANG_TIDY` | OFF | Enable clang-tidy |
| `CPP_QUICK_STARTER_ENABLE_CPPCHECK` | OFF | Enable cppcheck |
| `CPP_QUICK_STARTER_BUILD_TESTS` | ON | Build tests |
| `CPP_QUICK_STARTER_BUILD_BENCHMARKS` | OFF | Build benchmarks |
| `CPP_QUICK_STARTER_BUILD_EXAMPLES` | ON | Build examples |
| `CPP_QUICK_STARTER_BUILD_DOCS` | OFF | Build documentation |
<!-- [/EN] -->

<!-- [ZH] -->
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
<!-- [/ZH] -->

## CMake Presets / CMake 预设

<!-- [EN] -->
| Preset | Description | Platform |
|--------|-------------|----------|
| `ninja-debug` | Debug with Ninja | All |
| `ninja-release` | Release with Ninja | All |
| `ninja-ci` | CI build with warnings as errors | All |
| `ninja-sanitize` | Debug with sanitizers | Unix |
| `vs-debug` | Visual Studio Debug | Windows |
| `vs-release` | Visual Studio Release | Windows |
| `vcpkg-debug` | With vcpkg toolchain | All |
<!-- [/EN] -->

<!-- [ZH] -->
| 预设 | 描述 | 平台 |
|------|------|------|
| `ninja-debug` | Ninja 调试构建 | 全平台 |
| `ninja-release` | Ninja 发布构建 | 全平台 |
| `ninja-ci` | CI 构建（警告视为错误） | 全平台 |
| `ninja-sanitize` | 带内存检测的调试构建 | Unix |
| `vs-debug` | Visual Studio 调试 | Windows |
| `vs-release` | Visual Studio 发布 | Windows |
| `vcpkg-debug` | 使用 vcpkg 工具链 | 全平台 |
<!-- [/ZH] -->

## CLI Scaffolding Tool / CLI 脚手架工具

<!-- [EN] -->
The project provides a beautiful interactive CLI tool inspired by npm/yarn:
<!-- [/EN] -->

<!-- [ZH] -->
项目提供了美观的交互式 CLI 工具，灵感来自 npm/yarn：
<!-- [/ZH] -->

```bash
# Interactive project initialization / 交互式项目初始化
python scripts/cqs.py init

# Add new module / 添加新模块
python scripts/cqs.py add module

# Add dependency / 添加依赖
python scripts/cqs.py add dep

# Check development environment / 检查开发环境
python scripts/cqs.py doctor

# Show project information / 显示项目信息
python scripts/cqs.py info
```

### Build System Integration / 构建系统集成

<!-- [EN] -->
CLI tools are integrated into CMake and xmake:
<!-- [/EN] -->

<!-- [ZH] -->
CLI 工具已集成到 CMake 和 xmake：
<!-- [/ZH] -->

```bash
# CMake targets / CMake 目标
cmake --build build --target format       # Format code / 格式化代码
cmake --build build --target format-check # Check format / 检查格式
cmake --build build --target doctor       # Check environment / 检查环境
cmake --build build --target add-module   # Add module / 添加模块
cmake --build build --target add-dep      # Add dependency / 添加依赖

# xmake tasks / xmake 任务
xmake format           # Format code / 格式化代码
xmake format -c        # Check format / 检查格式
xmake doctor           # Check environment / 检查环境
xmake add-module       # Add module / 添加模块
xmake add-dep          # Add dependency / 添加依赖
xmake tasks            # List all tasks / 列出所有任务
```

## Scripts / 工具脚本

<!-- [EN] -->
Cross-platform scripts for common development tasks:

| Script | Unix | Windows | Description |
|--------|------|---------|-------------|
| Setup | `./scripts/setup.sh` | `.\scripts\setup.ps1` | Check development environment |
| Build | `./scripts/build.sh` | `.\scripts\build.ps1` | Configure and build project |
| Test | `./scripts/test.sh` | `.\scripts\test.ps1` | Run tests |
| Format | `./scripts/format.sh` | `.\scripts\format.ps1` | Format code with clang-format |
| Clean | `./scripts/clean.sh` | `.\scripts\clean.ps1` | Clean build artifacts |
<!-- [/EN] -->

<!-- [ZH] -->
跨平台脚本支持常见开发任务：

| 脚本 | Unix | Windows | 描述 |
|------|------|---------|------|
| 环境检查 | `./scripts/setup.sh` | `.\scripts\setup.ps1` | 检查开发环境 |
| 构建 | `./scripts/build.sh` | `.\scripts\build.ps1` | 配置并构建项目 |
| 测试 | `./scripts/test.sh` | `.\scripts\test.ps1` | 运行测试 |
| 格式化 | `./scripts/format.sh` | `.\scripts\format.ps1` | 格式化代码 |
| 清理 | `./scripts/clean.sh` | `.\scripts\clean.ps1` | 清理构建产物 |
<!-- [/ZH] -->

## Next Steps / 下一步

<!-- [EN] -->
- Read the [Scaffolding Guide](scaffolding.md) for CLI tool details
- Read the [API Documentation](api/index.md)
- Check out [Examples](../examples/)
- See [Contributing Guidelines](../CONTRIBUTING.md)
- Learn about [Code Quality](guides/code-quality.md) tools
<!-- [/EN] -->

<!-- [ZH] -->
- 阅读 [脚手架指南](scaffolding.md) 了解 CLI 工具详情
- 阅读 [API 文档](api/index.md)
- 查看 [示例代码](../examples/)
- 参阅 [贡献指南](../CONTRIBUTING.md)
- 了解 [代码质量](guides/code-quality.md) 工具
<!-- [/ZH] -->
