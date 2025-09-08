# Benchmarking

Feluda includes a benchmarking system that measures performance characteristics of all operators, helping developers optimize performance and maintain consistent standards.

## Quick Start

### Run All Benchmarks

```bash
cd benchmark
python main.py
```

Generates timestamped reports in `benchmark/results/`.

### Run Specific Operator

```python
from benchmark.operators import cluster_embeddings
from benchmark.report import BenchmarkReport

results = cluster_embeddings.benchmark()
report = BenchmarkReport()
report.extend(results)
report.save_json("results.json")
```

## System Components

### 1. Profiler Engine

Measures execution time, memory usage, and CPU time:

```python
from benchmark.profiler import Profiler

# Profile a function
@Profiler.profile
def my_function():
    # Your code here
    pass

# Benchmark an operator
result = Profiler.benchmark_operator(
    operator_class=MyOperator,
    operator_name="my_operator",
    runtime_kwargs={"input": "test_data"}
)
```

**Features:**
- System information capture (CPU, memory, platform)
- Memory usage tracking with peak detection
- Wall clock and CPU time measurement

### 2. Data Generator

Creates synthetic datasets for testing:

```python
from benchmark.data_generator import DataGenerator

# Generate embeddings
embeddings = DataGenerator.generate_embeddings(1000, 512)

# Generate clustered data
embeddings, labels = DataGenerator.generate_embeddings_with_clusters(
    num_clusters=5, samples_per_cluster=200, dim=512
)

# Generate test images
images = DataGenerator.generate_test_images("test_images/")
```

**Dataset Types:**

- **Embeddings**: 100 to 100,000 samples, 256 to 2048 dimensions
- **Images**: 128x128 to 4K resolutions, RGB/grayscale modes
- **Clustered Data**: Known cluster structures for validation

### 3. Operator Benchmarks

Each operator has a dedicated benchmark:

```python
def benchmark() -> list[dict]:
    """Benchmark the ClusterEmbeddings operator."""
    results = []

    # Test with different dataset sizes
    for n_clusters in [3, 5, 10]:
        embeddings, labels = DataGenerator.generate_embeddings_with_clusters(
            num_clusters=n_clusters, samples_per_cluster=200
        )

        result = Profiler.benchmark_operator(
            operator_class=ClusterEmbeddings,
            operator_name=f"cluster_embeddings_{n_clusters}clusters",
            runtime_kwargs={"input_data": embeddings}
        )

        result["data_description"] = f"{n_clusters} clusters, 200 samples each"
        results.append(result)

    return results
```

### 4. Report Generation

Creates comprehensive reports:

```python
from benchmark.report import BenchmarkReport

report = BenchmarkReport()
report.extend(benchmark_results)
report.save_json("results.json")
report.save_markdown("results.md")
```

## Example: Creating a New Benchmark

### 1. Create Benchmark File

```python
# benchmark/operators/my_operator.py
from benchmark.data_generator import DataGenerator
from benchmark.profiler import Profiler
from feluda.operators import MyOperator

def benchmark() -> list[dict]:
    """Benchmark the MyOperator."""
    results = []

    # Test configurations
    configs = [
        {"param1": "value1", "param2": 10},
        {"param1": "value2", "param2": 20}
    ]

    for config in configs:
        result = Profiler.benchmark_operator(
            operator_class=MyOperator,
            operator_name="my_operator",
            runtime_kwargs={"input": "test_data", **config}
        )

        result["data_description"] = f"config: {config}"
        results.append(result)

    return results
```

### 2. Register the Operator

Add to `benchmark/operators/__init__.py`:

```python
from . import my_operator

all_operators = [
    # ... existing operators
    my_operator,
]
```

## Performance Metrics

### Execution Metrics

- **Execution Time**: Total wall clock time
- **CPU Time**: Actual CPU processing time
- **Memory Change**: Net memory allocation/deallocation
- **Peak Memory**: Maximum memory usage

### Quality Metrics

- **Success Rate**: Percentage of successful runs
- **Error Details**: Specific failure reasons
- **Consistency**: Standard deviation of performance

## Understanding Results

### JSON Report Structure

```json
{
  "system_info": {
    "platform": "macOS-14.6.0-x86_64",
    "cpu_count": 8,
    "total_memory_gb": 16.0
  },
  "statistics": {
    "cluster_embeddings_kmeans": {
      "avg_execution_time": 0.045,
      "avg_memory_change": 2.45,
      "success_rate": 1.0
    }
  }
}
```

### Markdown Report

Provides human-readable summaries with:

- System configuration details
- Per-operator performance statistics
- Success rates and error information

## Dependencies

```bash
pip install psutil memory_profiler numpy pillow
```
