# Benchmark Report

Generated: 2025-08-22T00:37:31.805181

## System Information

- Platform: macOS-15.6-arm64-arm-64bit-Mach-O
- Processor: arm
- CPU Count: 10
- Total Memory: 16.00 GB
- Python Version: 3.13.7

## Operator Statistics

### cluster_embeddings_agglomerative

- Total Runs: 3
- Success Rate: 100.0%
- Avg Execution Time: 1.283s
- Min/Max Time: 1.210s / 1.329s
- Avg Memory Change: 18.64 MB
- Peak Memory: 369.08 MB

### cluster_embeddings_dbscan

- Total Runs: 3
- Success Rate: 100.0%
- Avg Execution Time: 1.330s
- Min/Max Time: 1.311s / 1.357s
- Avg Memory Change: 32.76 MB
- Peak Memory: 343.64 MB

### cluster_embeddings_kmeans

- Total Runs: 3
- Success Rate: 100.0%
- Avg Execution Time: 1.356s
- Min/Max Time: 1.116s / 1.482s
- Avg Memory Change: 3.91 MB
- Peak Memory: 317.58 MB

## Detailed Results

### cluster_embeddings_kmeans - clustered_3clusters - kmeans
- Execution Time: 1.116s
- Memory Change: 11.58 MB
- Peak Memory: 183.88 MB
- CPU Time: 0.109s

### cluster_embeddings_dbscan - clustered_3clusters - dbscan
- Execution Time: 1.311s
- Memory Change: 59.80 MB
- Peak Memory: 250.50 MB
- CPU Time: 0.536s

### cluster_embeddings_agglomerative - clustered_3clusters - agglomerative
- Execution Time: 1.210s
- Memory Change: 25.22 MB
- Peak Memory: 280.16 MB
- CPU Time: 0.513s

### cluster_embeddings_kmeans - clustered_5clusters - kmeans
- Execution Time: 1.469s
- Memory Change: 0.05 MB
- Peak Memory: 282.77 MB
- CPU Time: 0.130s

### cluster_embeddings_dbscan - clustered_5clusters - dbscan
- Execution Time: 1.357s
- Memory Change: 15.39 MB
- Peak Memory: 303.11 MB
- CPU Time: 0.636s

### cluster_embeddings_agglomerative - clustered_5clusters - agglomerative
- Execution Time: 1.329s
- Memory Change: 7.69 MB
- Peak Memory: 316.64 MB
- CPU Time: 0.642s

### cluster_embeddings_kmeans - clustered_10clusters - kmeans
- Execution Time: 1.482s
- Memory Change: 0.11 MB
- Peak Memory: 317.58 MB
- CPU Time: 0.132s

### cluster_embeddings_dbscan - clustered_10clusters - dbscan
- Execution Time: 1.322s
- Memory Change: 23.08 MB
- Peak Memory: 343.64 MB
- CPU Time: 0.638s

### cluster_embeddings_agglomerative - clustered_10clusters - agglomerative
- Execution Time: 1.311s
- Memory Change: 23.00 MB
- Peak Memory: 369.08 MB
- CPU Time: 0.634s
