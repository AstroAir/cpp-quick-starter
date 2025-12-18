# cpp-quick-starter

[![CI](https://github.com/AstroAir/cpp-quick-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/AstroAir/cpp-quick-starter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![C++20](https://img.shields.io/badge/C%2B%2B-20-blue.svg)](https://isocpp.org/std/the-standard)
[![Template](https://img.shields.io/badge/Template-Repository-green.svg)](https://github.com/AstroAir/cpp-quick-starter/generate)

[English](README.md) | [中文](README_CN.md)

A modern C++20 project template with best practices for quick project bootstrapping.

## ✨ Features

- **Modern C++20** - Leverages latest C++ standard features
- **Multiple Build Systems** - CMake, xmake support
- **Package Managers** - vcpkg, Conan integration
- **Cross-Platform** - Windows, Linux, macOS support with platform-specific presets
- **Scaffolding Tools** - Project initialization scripts for easy customization
- **Testing** - Google Test for unit and integration tests
- **Benchmarking** - Google Benchmark support
- **Code Quality** - clang-format, clang-tidy, cppcheck
- **CI/CD** - GitHub Actions workflows
- **Documentation** - Doxygen + MkDocs

## 🚀 Use This Template

### Option 1: GitHub Template (Recommended)

Click **"Use this template"** button on GitHub or:

```bash
gh repo create my-project --template AstroAir/cpp-quick-starter
```

### Option 2: Clone and Initialize

```bash
git clone https://github.com/AstroAir/cpp-quick-starter.git my-project
cd my-project
python scripts/init-project.py "MyProject" --reset-git
```

### Initialize Your Project

```bash
# Basic initialization
python scripts/init-project.py "MyAwesomeLib"

# With all options
python scripts/init-project.py "MyAwesomeLib" \
    --author "Your Name" \
    --description "My awesome C++ library" \
    --reset-git
```

This will rename all project references and set up a fresh project for you.

## 📁 Project Structure

```text
cpp-quick-starter/
├── .github/                    # GitHub configurations
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   └── workflows/              # CI/CD workflows
├── benchmarks/                 # Benchmark tests
├── cmake/                      # CMake modules
│   ├── CompilerWarnings.cmake
│   ├── Conan.cmake
│   ├── Doxygen.cmake
│   ├── Sanitizers.cmake
│   └── StaticAnalyzers.cmake
├── docs/                       # Documentation
│   ├── api/
│   └── guides/
├── examples/                   # Example code
├── include/                    # Public headers
│   └── project_name/
│       ├── core/
│       │   └── greeting.hpp
│       └── utils/
│           └── string_utils.hpp
├── scripts/                    # Utility scripts
├── src/                        # Source files
│   ├── core/
│   │   └── greeting.cpp
│   ├── utils/
│   │   └── string_utils.cpp
│   └── main.cpp
├── tests/                      # Test files
│   ├── integration/
│   └── unit/
├── .clang-format               # Code formatting rules
├── .clang-tidy                 # Static analysis rules
├── .clangd                     # Clangd configuration
├── CMakeLists.txt              # CMake build configuration
├── CMakePresets.json           # CMake presets
├── conanfile.txt               # Conan dependencies
├── vcpkg.json                  # vcpkg dependencies
└── xmake.lua                   # xmake build configuration
```

## 🚀 Quick Start

### Prerequisites

- C++20 compatible compiler (GCC 10+, Clang 10+, MSVC 2019+)
- CMake 3.21+ or xmake
- (Optional) vcpkg or Conan for package management

### Check Your Environment

```bash
# Unix (Linux/macOS)
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1
```

### Build with Scripts (Cross-Platform)

```bash
# Unix
./scripts/build.sh                    # Default preset
./scripts/build.sh ninja-release      # Release build
./scripts/build.sh --clean            # Clean build

# Windows PowerShell
.\scripts\build.ps1
.\scripts\build.ps1 -Preset ninja-release
.\scripts\build.ps1 -Clean
```

### Build with CMake Presets

```bash
# Configure and build
cmake --preset ninja-debug
cmake --build --preset ninja-debug

# Run tests
ctest --preset ninja-debug

# Or use workflow presets (CMake 3.25+)
cmake --workflow --preset dev      # configure + build + test
cmake --workflow --preset ci       # with warnings as errors
cmake --workflow --preset release  # release build
```

### Build with xmake

```bash
xmake                              # Configure and build
xmake run cpp_quick_starter_app    # Run application
xmake run unit_tests               # Run tests
```

### CMake Presets

| Preset | Description | Platform |
|--------|-------------|----------|
| `ninja-debug` | Debug build with Ninja | All |
| `ninja-release` | Release build with Ninja | All |
| `ninja-ci` | CI build with warnings as errors | All |
| `ninja-sanitize` | Debug with sanitizers | Unix |
| `vs-debug` | Visual Studio Debug | Windows |
| `vs-release` | Visual Studio Release | Windows |
| `macos-debug` | macOS Debug | macOS |
| `linux-debug` | Linux Debug | Linux |
| `linux-clang-debug` | Linux with Clang | Linux |
| `vcpkg-debug` | With vcpkg toolchain | All |

### CMake Options

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

## 📦 Package Management

### vcpkg

```bash
# Install dependencies
vcpkg install

# Configure with vcpkg toolchain
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Conan

```bash
# Install dependencies
conan install . --output-folder=build --build=missing

# Configure with Conan toolchain
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```

## 🧪 Testing

```bash
# Run all tests with CTest
ctest --test-dir build --output-on-failure

# Or run test executables directly
./build/tests/unit_tests
./build/tests/integration_tests
```

## 📊 Benchmarking

```bash
# Enable benchmarks
cmake -B build -S . -DCPP_QUICK_STARTER_BUILD_BENCHMARKS=ON
cmake --build build

# Run benchmarks
./build/benchmarks/benchmarks
```

## 🛠️ CLI Scaffolding Tool

Beautiful interactive CLI for project scaffolding (inspired by npm/yarn):

```bash
# Interactive project initialization
python scripts/cqs.py init

# Add a new module
python scripts/cqs.py add module

# Add a dependency
python scripts/cqs.py add dep

# Check development environment
python scripts/cqs.py doctor

# Show project info
python scripts/cqs.py info
```

### Build System Integration

All CLI tools are integrated into CMake and xmake:

```bash
# CMake targets
cmake --build build --target format       # Format code
cmake --build build --target format-check # Check formatting
cmake --build build --target doctor       # Check environment
cmake --build build --target add-module   # Add module (interactive)
cmake --build build --target add-dep      # Add dependency (interactive)

# xmake tasks
xmake format           # Format code
xmake format -c        # Check formatting
xmake doctor           # Check environment
xmake add-module       # Add module (interactive)
xmake add-dep          # Add dependency (interactive)
xmake tasks            # List all tasks
```

### CLI Commands

| Command | CMake Target | xmake Task |
|---------|--------------|------------|
| `cqs init` | - | `xmake init` |
| `cqs add module` | `add-module` | `xmake add-module` |
| `cqs add dep` | `add-dep` | `xmake add-dep` |
| `cqs doctor` | `doctor` | `xmake doctor` |
| `cqs info` | `info` | `xmake info` |
| Format code | `format` | `xmake format` |
| Check format | `format-check` | `xmake format -c` |

## 📜 Scripts

Cross-platform scripts are available for common tasks:

| Script | Unix | Windows | Description |
|--------|------|---------|-------------|
| Setup | `./scripts/setup.sh` | `.\scripts\setup.ps1` | Check development environment |
| Build | `./scripts/build.sh` | `.\scripts\build.ps1` | Configure and build project |
| Test | `./scripts/test.sh` | `.\scripts\test.ps1` | Run tests |
| Format | `./scripts/format.sh` | `.\scripts\format.ps1` | Format code with clang-format |
| Clean | `./scripts/clean.sh` | `.\scripts\clean.ps1` | Clean build artifacts |
| Init | `python scripts/init-project.py` | `python scripts\init-project.py` | Initialize new project (non-interactive) |

## 🔍 Code Quality

### Format Code

```bash
# Unix
./scripts/format.sh              # Format all files
./scripts/format.sh --check      # Check without modifying (CI mode)

# Windows
.\scripts\format.ps1
.\scripts\format.ps1 -Check
```

### Static Analysis

```bash
# Enable clang-tidy
cmake -B build -S . -DCPP_QUICK_STARTER_ENABLE_CLANG_TIDY=ON

# Enable cppcheck
cmake -B build -S . -DCPP_QUICK_STARTER_ENABLE_CPPCHECK=ON

# Run with sanitizers
cmake --preset ninja-sanitize
cmake --build --preset ninja-sanitize
```

## 📚 Documentation

```bash
# Build documentation
cmake -B build -S . -DCPP_QUICK_STARTER_BUILD_DOCS=ON
cmake --build build --target docs

# Serve MkDocs locally
mkdocs serve
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Test](https://github.com/google/googletest)
- [Google Benchmark](https://github.com/google/benchmark)
- [CMake](https://cmake.org/)
- [xmake](https://xmake.io/)
