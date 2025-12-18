# xmake Guide / xmake 指南

<!-- [EN] -->
This project provides full xmake build support with custom task integration.
<!-- [/EN] -->

<!-- [ZH] -->
本项目提供完整的 xmake 构建支持，包括自定义任务集成。
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

## Basic Commands / 基本命令

```bash
# Configure (debug mode) / 配置（调试模式）
xmake f -m debug

# Configure (release mode) / 配置（发布模式）
xmake f -m release

# Build / 构建
xmake

# Run application / 运行应用程序
xmake run cpp_quick_starter_app

# Run tests / 运行测试
xmake run unit_tests
xmake run integration_tests
```

## Build Options / 构建选项

<!-- [EN] -->
| Option | Default | Description |
|--------|---------|-------------|
| `--build_tests` | yes | Build tests |
| `--build_benchmarks` | no | Build benchmarks |
| `--build_examples` | yes | Build examples |
<!-- [/EN] -->

<!-- [ZH] -->
| 选项 | 默认值 | 描述 |
|------|--------|------|
| `--build_tests` | yes | 构建测试 |
| `--build_benchmarks` | no | 构建基准测试 |
| `--build_examples` | yes | 构建示例 |
<!-- [/ZH] -->

```bash
# Enable all options / 启用所有选项
xmake f -m release --build_tests=y --build_benchmarks=y --build_examples=y

# Disable tests / 禁用测试
xmake f --build_tests=n
```

## Custom Tasks / 自定义任务

<!-- [EN] -->
xmake integrates all CLI functionality:
<!-- [/EN] -->

<!-- [ZH] -->
xmake 集成了所有 CLI 功能：
<!-- [/ZH] -->

### Build & Test / 构建与测试

```bash
xmake test              # Run tests / 运行测试
xmake test -d           # Verbose output / 详细输出
xmake test -f "pattern" # Filter tests / 过滤测试
xmake format            # Format code / 格式化代码
xmake format -c         # Check format (CI) / 检查格式
xmake clean-all         # Clean all artifacts / 清理所有
```

### Documentation / 文档

```bash
xmake docs              # Build MkDocs docs / 构建 MkDocs 文档
xmake docs-serve        # Serve docs locally / 本地预览文档
```

### CLI Scaffolding / CLI 脚手架

```bash
xmake init              # Interactive project init / 交互式项目初始化
xmake add-module        # Add new module / 添加新模块
xmake add-dep           # Add dependency / 添加依赖
xmake info              # Show project info / 显示项目信息
xmake doctor            # Check environment / 检查开发环境
xmake setup             # Check dev setup / 检查开发环境设置
xmake cli [command]     # Run CLI command / 运行 CLI 命令
```

### List All Tasks / 查看所有任务

```bash
xmake tasks             # List all custom tasks / 列出所有自定义任务
```

## Quick Reference / 快速参考

<!-- [EN] -->
| Task | Command | Description |
|------|---------|-------------|
| Build | `xmake` | Configure and build project |
| Run | `xmake run <target>` | Run specified target |
| Test | `xmake test` | Run all tests |
| Format | `xmake format` | Format code |
| Clean | `xmake clean` | Clean build artifacts |
| Docs | `xmake docs` | Build documentation |
| Check env | `xmake doctor` | Check development environment |
<!-- [/EN] -->

<!-- [ZH] -->
| 任务 | 命令 | 描述 |
|------|------|------|
| 构建 | `xmake` | 配置并构建项目 |
| 运行 | `xmake run <target>` | 运行指定目标 |
| 测试 | `xmake test` | 运行所有测试 |
| 格式化 | `xmake format` | 格式化代码 |
| 清理 | `xmake clean` | 清理构建产物 |
| 文档 | `xmake docs` | 构建文档 |
| 环境检查 | `xmake doctor` | 检查开发环境 |
<!-- [/ZH] -->
