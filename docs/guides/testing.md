# Testing Guide / 测试指南

<!-- [EN] -->
This project uses Google Test framework for unit and integration tests.
<!-- [/EN] -->

<!-- [ZH] -->
本项目使用 Google Test 框架进行单元测试和集成测试。
<!-- [/ZH] -->

## Test Structure / 测试结构

```
tests/
├── unit/                    # Unit tests / 单元测试
│   ├── main.cpp             # Test entry / 测试入口
│   ├── greeting_test.cpp    # greeting module tests / greeting 模块测试
│   └── string_utils_test.cpp # string_utils tests / string_utils 测试
└── integration/             # Integration tests / 集成测试
    ├── main.cpp             # Test entry / 测试入口
    └── smoke_test.cpp       # Smoke tests / 冒烟测试
```

## Using CMake / 使用 CMake

```bash
# Configure and build (tests enabled by default) / 配置并构建（测试默认启用）
cmake --preset ninja-debug
cmake --build --preset ninja-debug

# Run all tests / 运行所有测试
ctest --preset ninja-debug

# Run specific tests / 运行特定测试
ctest --preset ninja-debug -R "unit"      # Unit tests only / 只运行单元测试
ctest --preset ninja-debug -R "greeting"  # Tests containing greeting

# Verbose output / 详细输出
ctest --preset ninja-debug --output-on-failure
ctest --preset ninja-debug -V
```

## Using Scripts / 使用脚本

```bash
# Unix
./scripts/test.sh                    # Run all tests / 运行所有测试
./scripts/test.sh --filter "unit*"   # Filter tests / 过滤测试
./scripts/test.sh --verbose          # Verbose output / 详细输出
./scripts/test.sh --build            # Build then run / 构建后运行

# Windows PowerShell
.\scripts\test.ps1
.\scripts\test.ps1 -Filter "greeting*"
.\scripts\test.ps1 -Verbose -Build
```

## Using xmake / 使用 xmake

```bash
# Configure (tests enabled by default) / 配置（测试默认启用）
xmake f --build_tests=y
xmake

# Run tests / 运行测试
xmake run unit_tests
xmake run integration_tests

# Using xmake tasks / 使用 xmake 任务
xmake test              # Run all tests / 运行所有测试
xmake test -d           # Verbose output / 详细输出
xmake test -f "pattern" # Filter tests / 过滤测试
```

## Writing Tests / 编写测试

### Unit Test Example / 单元测试示例

```cpp
#include <gtest/gtest.h>
#include "project_name/utils/string_utils.hpp"

namespace project_name::test {

TEST(StringUtilsTest, ToUpperCase) {
    EXPECT_EQ(to_upper("hello"), "HELLO");
    EXPECT_EQ(to_upper(""), "");
}

class StringUtilsFixture : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code / 初始化代码
    }
    void TearDown() override {
        // Teardown code / 清理代码
    }
};

TEST_F(StringUtilsFixture, ComplexTest) {
    // Test using fixture / 使用 fixture 的测试
    EXPECT_TRUE(true);
}

}  // namespace project_name::test
```

## Disable Tests / 禁用测试

```bash
# CMake
cmake -B build -S . -DCPP_QUICK_STARTER_BUILD_TESTS=OFF

# xmake
xmake f --build_tests=n
```
