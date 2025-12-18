# cpp-quick-starter

<!-- [EN] -->
A modern C++20 project template with best practices for quick project bootstrapping.
<!-- [/EN] -->

<!-- [ZH] -->
现代化的 C++20 项目模板，集成最佳实践，助您快速启动新项目。
<!-- [/ZH] -->

## ✨ Features / 特性

<!-- [EN] -->
- **Modern C++20** - Leverages latest C++ standard features
- **Multiple Build Systems** - CMake, xmake support
- **Package Managers** - vcpkg, Conan integration
- **Cross-Platform** - Windows, Linux, macOS support
- **CLI Scaffolding Tool** - Interactive project init, module creation, dependency management
- **Testing** - Google Test for unit and integration tests
- **Benchmarking** - Google Benchmark support
- **Code Quality** - clang-format, clang-tidy, cppcheck
- **CI/CD** - GitHub Actions workflows
- **Documentation** - Doxygen + MkDocs
<!-- [/EN] -->

<!-- [ZH] -->
- **现代 C++20** - 使用最新 C++ 标准特性
- **多构建系统** - CMake、xmake 双支持
- **包管理器** - vcpkg、Conan 集成
- **跨平台** - Windows、Linux、macOS 全平台支持
- **CLI 脚手架工具** - 交互式项目初始化、模块添加、依赖管理
- **测试框架** - Google Test 单元测试和集成测试
- **性能基准** - Google Benchmark 支持
- **代码质量** - clang-format、clang-tidy、cppcheck
- **CI/CD** - GitHub Actions 工作流
- **文档生成** - Doxygen + MkDocs
<!-- [/ZH] -->

## 🚀 Quick Start / 快速开始

```bash
# Interactive project initialization / 交互式项目初始化
python scripts/cqs.py init

# Or use build presets / 或使用构建预设
cmake --preset ninja-debug
cmake --build --preset ninja-debug
ctest --preset ninja-debug
```

## 📖 Documentation / 文档导航

<!-- [EN] -->
- [Getting Started](getting-started.md) - Environment setup and first build
- [Scaffolding Guide](scaffolding.md) - CLI tools and scripts
- [CMake Guide](guides/cmake.md) - CMake options and presets
- [Code Quality](guides/code-quality.md) - Formatting and static analysis
<!-- [/EN] -->

<!-- [ZH] -->
- [快速入门](getting-started.md) - 环境配置与首次构建
- [脚手架指南](scaffolding.md) - CLI 工具与脚本使用
- [CMake 指南](guides/cmake.md) - CMake 选项与预设
- [代码质量](guides/code-quality.md) - 格式化与静态分析
<!-- [/ZH] -->
