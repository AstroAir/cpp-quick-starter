# CMake Guide / CMake 指南

<!-- [EN] -->
This project uses modern CMake (3.21+) with presets and workflows support.
<!-- [/EN] -->

<!-- [ZH] -->
本项目使用现代 CMake (3.21+) 组织代码，支持预设和工作流。
<!-- [/ZH] -->

## Build Targets / 构建目标

<!-- [EN] -->
| Target | Description |
|--------|-------------|
| `cpp_quick_starter` | Core static library |
| `cpp_quick_starter_app` | Sample executable |
| `unit_tests` | Unit tests |
| `integration_tests` | Integration tests |
| `benchmarks` | Performance benchmarks |
| `example_01` | Example program |
<!-- [/EN] -->

<!-- [ZH] -->
| 目标 | 描述 |
|------|------|
| `cpp_quick_starter` | 核心静态库 |
| `cpp_quick_starter_app` | 示例可执行程序 |
| `unit_tests` | 单元测试 |
| `integration_tests` | 集成测试 |
| `benchmarks` | 性能基准测试 |
| `example_01` | 示例程序 |
<!-- [/ZH] -->

## Common Commands / 常用命令

```bash
# Configure and build with presets / 使用预设配置和构建
cmake --preset ninja-debug
cmake --build --preset ninja-debug
ctest --preset ninja-debug

# Workflow presets (CMake 3.25+) / 工作流预设
cmake --workflow --preset dev      # Dev: configure + build + test / 开发
cmake --workflow --preset ci       # CI: warnings as errors / CI
cmake --workflow --preset release  # Release build / 发布构建
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
| `CPP_QUICK_STARTER_ENABLE_MKDOCS` | ON | Enable MkDocs targets |
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
| `CPP_QUICK_STARTER_ENABLE_MKDOCS` | ON | 启用 MkDocs 目标 |
<!-- [/ZH] -->

## CMake Presets / CMake 预设

<!-- [EN] -->
| Preset | Description | Platform |
|--------|-------------|----------|
| `ninja-debug` | Debug with Ninja | All |
| `ninja-release` | Release with Ninja | All |
| `ninja-ci` | CI build (warnings as errors) | All |
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

## Script Integration Targets / 脚本集成目标

<!-- [EN] -->
The project provides convenient development targets via `Scripts.cmake`:
<!-- [/EN] -->

<!-- [ZH] -->
项目通过 `Scripts.cmake` 模块提供便捷的开发任务目标：
<!-- [/ZH] -->

```bash
# Code quality / 代码质量
cmake --build build --target format        # Format code / 格式化代码
cmake --build build --target format-check  # Check format (CI) / 检查格式
cmake --build build --target lint          # Alias for format-check / 别名

# Clean / 清理
cmake --build build --target clean-all     # Clean all artifacts / 清理所有

# CLI tools / CLI 工具
cmake --build build --target doctor        # Check environment / 检查环境
cmake --build build --target info          # Project info / 项目信息
cmake --build build --target add-module    # Add module (interactive) / 添加模块
cmake --build build --target add-dep       # Add dependency / 添加依赖

# Documentation / 文档
cmake --build build --target docs          # Build all docs / 构建所有文档
cmake --build build --target doxygen       # Build Doxygen / 构建 Doxygen
cmake --build build --target mkdocs-build  # Build MkDocs / 构建 MkDocs
cmake --build build --target mkdocs-serve  # Serve docs locally / 本地预览
```

## Package Manager Integration / 包管理器集成

### vcpkg

```bash
# Use vcpkg preset / 使用 vcpkg 预设
cmake --preset vcpkg-debug

# Or manually specify toolchain / 或手动指定工具链
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Conan

```bash
# Install dependencies / 安装依赖
conan install . --output-folder=build --build=missing

# Use Conan toolchain / 使用 Conan 工具链
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```
