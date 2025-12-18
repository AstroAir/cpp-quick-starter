# Code Quality / 代码质量

<!-- [EN] -->
This project integrates multiple code quality tools to ensure code standards and safety.
<!-- [/EN] -->

<!-- [ZH] -->
本项目集成多种代码质量工具，确保代码规范和安全。
<!-- [/ZH] -->

## Code Formatting / 代码格式化

### Using Scripts (Recommended) / 使用脚本（推荐）

```bash
# Unix
./scripts/format.sh              # Format all files / 格式化所有文件
./scripts/format.sh --check      # Check only (CI mode) / 仅检查（CI 模式）

# Windows PowerShell
.\scripts\format.ps1
.\scripts\format.ps1 -Check
```

### Using Build System / 使用构建系统

```bash
# CMake
cmake --build build --target format        # Format code / 格式化代码
cmake --build build --target format-check  # Check format / 检查格式

# xmake
xmake format           # Format code / 格式化代码
xmake format -c        # Check format / 检查格式
```

### Using clang-format Directly / 直接使用 clang-format

```bash
clang-format -i src/**/*.cpp include/**/*.hpp tests/**/*.cpp examples/**/*.cpp
```

## Static Analysis / 静态分析

### clang-tidy

<!-- [EN] -->
Ensure `compile_commands.json` is generated:
<!-- [/EN] -->

<!-- [ZH] -->
确保生成 `compile_commands.json`：
<!-- [/ZH] -->

```bash
# Enable clang-tidy / 启用 clang-tidy
cmake --preset ninja-debug -DCPP_QUICK_STARTER_ENABLE_CLANG_TIDY=ON
cmake --build --preset ninja-debug

# Run manually / 手动运行
clang-tidy -p build/ninja-debug src/main.cpp
```

### cppcheck

```bash
# Enable cppcheck / 启用 cppcheck
cmake -B build -S . -DCPP_QUICK_STARTER_ENABLE_CPPCHECK=ON
cmake --build build
```

## Sanitizers / 内存检测

<!-- [EN] -->
Use the sanitize preset to enable memory detection tools:
<!-- [/EN] -->

<!-- [ZH] -->
使用 sanitize 预设启用内存检测工具：
<!-- [/ZH] -->

```bash
cmake --preset ninja-sanitize
cmake --build --preset ninja-sanitize
ctest --preset ninja-sanitize
```

<!-- [EN] -->
Supported Sanitizers:

- **AddressSanitizer** - Detects memory access errors
- **UndefinedBehaviorSanitizer** - Detects undefined behavior
<!-- [/EN] -->

<!-- [ZH] -->
支持的 Sanitizers：

- **AddressSanitizer** - 检测内存访问错误
- **UndefinedBehaviorSanitizer** - 检测未定义行为
<!-- [/ZH] -->

## Environment Check / 环境检查

<!-- [EN] -->
Use the `doctor` command to check if code quality tools are installed:
<!-- [/EN] -->

<!-- [ZH] -->
使用 `doctor` 命令检查代码质量工具是否已安装：
<!-- [/ZH] -->

```bash
# CLI
python scripts/cqs.py doctor

# CMake
cmake --build build --target doctor

# xmake
xmake doctor
```

## CI Integration / CI 集成

<!-- [EN] -->
The project CI workflow automatically performs code quality checks:
<!-- [/EN] -->

<!-- [ZH] -->
项目 CI 工作流自动执行代码质量检查：
<!-- [/ZH] -->

```bash
# Use CI preset (warnings as errors) / 使用 CI 预设（警告视为错误）
cmake --preset ninja-ci
cmake --build --preset ninja-ci
ctest --preset ninja-ci
```

## Configuration Files / 配置文件

<!-- [EN] -->
| File | Description |
|------|-------------|
| `.clang-format` | clang-format formatting rules |
| `.clang-tidy` | clang-tidy check rules |
| `.clangd` | Clangd LSP configuration |
| `.editorconfig` | Editor common configuration |
<!-- [/EN] -->

<!-- [ZH] -->
| 文件 | 描述 |
|------|------|
| `.clang-format` | clang-format 格式化规则 |
| `.clang-tidy` | clang-tidy 检查规则 |
| `.clangd` | Clangd LSP 配置 |
| `.editorconfig` | 编辑器通用配置 |
<!-- [/ZH] -->
