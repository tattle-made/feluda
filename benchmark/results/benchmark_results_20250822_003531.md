# Benchmark Report

Generated: 2025-08-22T00:34:11.788553

## System Information

- Platform: macOS-15.6-arm64-arm-64bit-Mach-O
- Processor: arm
- CPU Count: 10
- Total Memory: 16.00 GB
- Python Version: 3.13.7

## Operator Statistics

### dimension_reduction_tsne

- Total Runs: 4
- Success Rate: 100.0%
- Avg Execution Time: 11.869s
- Min/Max Time: 2.523s / 22.809s
- Avg Memory Change: 47.63 MB
- Peak Memory: 821.25 MB

### dimension_reduction_umap

- Total Runs: 4
- Success Rate: 100.0%
- Avg Execution Time: 7.768s
- Min/Max Time: 4.354s / 11.065s
- Avg Memory Change: 32.17 MB
- Peak Memory: 886.48 MB

## Detailed Results

### dimension_reduction_tsne - small_500x512 - tsne
- Execution Time: 2.523s
- Memory Change: 17.84 MB
- Peak Memory: 336.75 MB
- CPU Time: 7.597s

### dimension_reduction_umap - small_500x512 - umap
- Execution Time: 4.354s
- Memory Change: 34.00 MB
- Peak Memory: 375.55 MB
- CPU Time: 2.546s

### dimension_reduction_tsne - medium_2000x512 - tsne
- Execution Time: 9.561s
- Memory Change: 53.88 MB
- Peak Memory: 460.58 MB
- CPU Time: 73.561s

### dimension_reduction_umap - medium_2000x512 - umap
- Execution Time: 4.720s
- Memory Change: 40.02 MB
- Peak Memory: 507.41 MB
- CPU Time: 2.762s

### dimension_reduction_tsne - large_5000x512 - tsne
- Execution Time: 12.582s
- Memory Change: -26.03 MB
- Peak Memory: 632.53 MB
- CPU Time: 98.041s

### dimension_reduction_umap - large_5000x512 - umap
- Execution Time: 10.932s
- Memory Change: 8.38 MB
- Peak Memory: 609.11 MB
- CPU Time: 8.778s

### dimension_reduction_tsne - xlarge_10000x512 - tsne
- Execution Time: 22.809s
- Memory Change: 144.84 MB
- Peak Memory: 821.25 MB
- CPU Time: 192.297s

### dimension_reduction_umap - xlarge_10000x512 - umap
- Execution Time: 11.065s
- Memory Change: 46.28 MB
- Peak Memory: 886.48 MB
- CPU Time: 9.073s
