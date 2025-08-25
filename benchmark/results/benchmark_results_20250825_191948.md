# Benchmark Report

Generated: 2025-08-25T19:19:36.446474

## System Information

- Platform: macOS-15.6.1-arm64-arm-64bit-Mach-O
- Processor: arm
- CPU Count: 10
- Total Memory: 16.00 GB
- Python Version: 3.13.7

## Operator Statistics

| Operator | Total Runs | Success Rate (%) | Avg Time (s) | Min Time (s) | Max Time (s) | Std Time (s) | Avg Mem Change (MB) | Peak Mem (MB) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cluster_embeddings_agglomerative | 3 | 100.0 | 1.280 | 1.172 | 1.368 | 0.081 | 16.48 | 371.16 |
| cluster_embeddings_dbscan | 3 | 100.0 | 1.288 | 1.175 | 1.387 | 0.087 | 33.07 | 369.08 |
| cluster_embeddings_kmeans | 3 | 100.0 | 1.455 | 1.428 | 1.494 | 0.028 | 2.63 | 343.02 |

## Detailed Results

| Operator | Data | Status | Exec Time (s) | Mem Change (MB) | Peak Mem (MB) | CPU Time (s) | Error |
|---|---|---|---:|---:|---:|---:|---|
| cluster_embeddings_kmeans | clustered_3clusters - kmeans | success | 1.428 | 7.75 | 190.52 | 0.119 |  |
| cluster_embeddings_dbscan | clustered_3clusters - dbscan | success | 1.175 | 40.98 | 238.25 | 0.513 |  |
| cluster_embeddings_agglomerative | clustered_3clusters - agglomerative | success | 1.172 | 18.70 | 261.58 | 0.512 |  |
| cluster_embeddings_kmeans | clustered_5clusters - kmeans | success | 1.494 | 0.08 | 264.50 | 0.128 |  |
| cluster_embeddings_dbscan | clustered_5clusters - dbscan | success | 1.303 | 35.19 | 303.75 | 0.631 |  |
| cluster_embeddings_agglomerative | clustered_5clusters - agglomerative | success | 1.298 | 30.69 | 337.09 | 0.636 |  |
| cluster_embeddings_kmeans | clustered_10clusters - kmeans | success | 1.444 | 0.06 | 343.02 | 0.129 |  |
| cluster_embeddings_dbscan | clustered_10clusters - dbscan | success | 1.387 | 23.05 | 369.08 | 0.684 |  |
| cluster_embeddings_agglomerative | clustered_10clusters - agglomerative | success | 1.368 | 0.06 | 371.16 | 0.665 |  |
