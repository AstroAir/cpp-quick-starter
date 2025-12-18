# Benchmarks / 性能基准测试

<!-- [EN] -->
This project uses Google Benchmark framework for performance benchmarking.
<!-- [/EN] -->

<!-- [ZH] -->
本项目使用 Google Benchmark 框架进行性能基准测试。
<!-- [/ZH] -->

## Benchmark Structure / 基准测试结构

```
benchmarks/
├── CMakeLists.txt           # CMake configuration / CMake 配置
└── string_utils_bench.cpp   # string_utils benchmarks / string_utils 基准测试
```

## Using CMake / 使用 CMake

```bash
# Enable benchmarks / 启用基准测试
cmake --preset ninja-release -DCPP_QUICK_STARTER_BUILD_BENCHMARKS=ON
cmake --build --preset ninja-release

# Run benchmarks / 运行基准测试
./build/ninja-release/benchmarks/benchmarks

# Common options / 常用选项
./build/ninja-release/benchmarks/benchmarks --benchmark_filter="StringUtils"
./build/ninja-release/benchmarks/benchmarks --benchmark_format=json
./build/ninja-release/benchmarks/benchmarks --benchmark_out=results.json
```

## Using xmake / 使用 xmake

```bash
# Enable benchmarks / 启用基准测试
xmake f -m release --build_benchmarks=y
xmake

# Run benchmarks / 运行基准测试
xmake run benchmarks
```

## Writing Benchmarks / 编写基准测试

### Basic Example / 基本示例

```cpp
#include <benchmark/benchmark.h>
#include "project_name/utils/string_utils.hpp"

static void BM_ToUpper(benchmark::State& state) {
    std::string input = "hello world";
    for (auto _ : state) {
        auto result = project_name::to_upper(input);
        benchmark::DoNotOptimize(result);
    }
}
BENCHMARK(BM_ToUpper);

static void BM_ToUpperWithSize(benchmark::State& state) {
    std::string input(state.range(0), 'a');
    for (auto _ : state) {
        auto result = project_name::to_upper(input);
        benchmark::DoNotOptimize(result);
    }
    state.SetComplexityN(state.range(0));
}
BENCHMARK(BM_ToUpperWithSize)
    ->Range(8, 8<<10)
    ->Complexity(benchmark::oN);

BENCHMARK_MAIN();
```

## Best Practices / 最佳实践

<!-- [EN] -->
- Use **Release** mode for accurate results
- Use `benchmark::DoNotOptimize()` to prevent compiler optimization
- Run multiple times to ensure stable results
- Use `--benchmark_repetitions=N` for repeated tests
<!-- [/EN] -->

<!-- [ZH] -->
- 使用 **Release** 模式运行基准测试以获得准确结果
- 使用 `benchmark::DoNotOptimize()` 防止编译器优化掉测试代码
- 多次运行以确保结果稳定
- 使用 `--benchmark_repetitions=N` 进行多次重复测试
<!-- [/ZH] -->
