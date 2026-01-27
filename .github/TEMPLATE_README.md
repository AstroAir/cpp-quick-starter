# Using this Template

This repository is designed to be used as a **GitHub Template Repository**. Here's how to get started with your new C++ project.

## Quick Start

### 1. Create Your Repository

Click the green **"Use this template"** button on GitHub, or use GitHub CLI:

```bash
gh repo create my-awesome-project --template AstroAir/cpp-quick-starter
```

### 2. Clone and Initialize

```bash
git clone https://github.com/YOUR_USERNAME/my-awesome-project.git
cd my-awesome-project

# Initialize with your project name
python scripts/init-project.py "MyAwesomeProject"

# Or with more options
python scripts/init-project.py "MyAwesomeProject" \
    --author "Your Name" \
    --description "My awesome C++ library" \
    --reset-git
```

### 3. Build and Test

```bash
# Using CMake presets
cmake --preset ninja-debug
cmake --build --preset ninja-debug
ctest --preset ninja-debug

# Or using the scripts
./scripts/build.sh          # Unix
.\scripts\build.ps1         # Windows
```

## What the Init Script Does

The `init-project.py` script:

1. **Renames** all project references from `cpp_quick_starter` to your project name
2. **Updates** CMakeLists.txt, xmake.lua, vcpkg.json, and other config files
3. **Renames** the include directory from `project_name/` to your project name
4. **Updates** all `#include` directives in source files
5. **Creates** a fresh CHANGELOG.md
6. **Optionally resets** git history for a clean start

## Customization Checklist

After initializing your project:

- [ ] Update `README.md` with your project description
- [ ] Update `LICENSE` with your name/organization
- [ ] Update `AUTHORS.md` with contributor information
- [ ] Modify `CONTRIBUTING.md` for your project's workflow
- [ ] Update `.github/CODEOWNERS` with your team
- [ ] Configure `.github/FUNDING.yml` if accepting sponsorships
- [ ] Review and adjust CI workflows in `.github/workflows/`
- [ ] Add your project-specific dependencies to `vcpkg.json` or `conanfile.txt`

## Available Scripts

| Script | Description |
| ------ | ----------- |
| `init-project.py` | Initialize project with new name |
| `build.sh` / `build.ps1` | Configure and build project |
| `test.sh` / `test.ps1` | Run tests |
| `format.sh` / `format.ps1` | Format code with clang-format |
| `clean.sh` / `clean.ps1` | Clean build artifacts |
| `setup.sh` / `setup.ps1` | Check development environment |

## Directory Structure After Init

```text
your-project/
├── include/your_project/     # Public headers (renamed)
├── src/                      # Source files
├── tests/                    # Unit and integration tests
├── benchmarks/               # Performance benchmarks
├── examples/                 # Example code
├── docs/                     # Documentation
├── scripts/                  # Build and utility scripts
├── cmake/                    # CMake modules
├── CMakeLists.txt            # CMake configuration (updated)
├── xmake.lua                 # xmake configuration (updated)
└── ...
```

## Need Help?

- Check the main [README.md](../README.md) for detailed documentation
- Open an issue on the template repository for template-related problems
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
