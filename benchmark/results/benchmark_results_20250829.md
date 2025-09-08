# Benchmark Report

Generated: 2025-08-28T23:55:24.834470

## System Information

- Platform: macOS-15.6.1-arm64-arm-64bit-Mach-O
- Processor: arm
- CPU Count: 10
- Total Memory: 16.00 GB
- Python Version: 3.13.7

## Operator Statistics

| Operator | Total Runs | Success Rate (%) | Avg Time (s) | Min Time (s) | Max Time (s) | Std Time (s) | Avg Mem Change (MB) | Peak Mem (MB) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| cluster_embeddings_agglomerative | 3 | 100.0 | 6.805 | 6.164 | 8.069 | 0.894 | 23.85 | 851.23 |
| cluster_embeddings_dbscan | 3 | 100.0 | 6.256 | 6.214 | 6.277 | 0.030 | -10.64 | 851.92 |
| cluster_embeddings_kmeans | 3 | 100.0 | 12.851 | 10.772 | 14.850 | 1.666 | -38.10 | 846.00 |
| detect_lewd_images | 11 | 100.0 | 8.863 | 6.579 | 9.632 | 0.817 | -18.47 | 1905.08 |
| detect_text_in_image | 11 | 100.0 | 9.381 | 5.869 | 15.024 | 2.735 | 0.54 | 1615.25 |
| dimension_reduction_tsne | 4 | 100.0 | 30.234 | 6.242 | 63.125 | 21.633 | 40.23 | 2008.08 |
| dimension_reduction_umap | 4 | 100.0 | 12.339 | 8.190 | 16.055 | 3.177 | 18.89 | 2041.16 |

## Detailed Results

| Operator | Data | Status | Exec Time (s) | Mem Change (MB) | Peak Mem (MB) | CPU Time (s) | Error |
|---|---|---|---:|---:|---:|---:|---|
| cluster_embeddings_kmeans | clustered_3clusters - kmeans | success | 10.772 | -114.27 | 833.44 | 0.159 |  |
| cluster_embeddings_dbscan | clustered_3clusters - dbscan | success | 6.277 | -45.19 | 783.95 | 0.530 |  |
| cluster_embeddings_agglomerative | clustered_3clusters - agglomerative | success | 8.069 | 48.06 | 791.03 | 0.517 |  |
| cluster_embeddings_kmeans | clustered_5clusters - kmeans | success | 12.932 | -0.08 | 798.42 | 0.136 |  |
| cluster_embeddings_dbscan | clustered_5clusters - dbscan | success | 6.214 | 13.16 | 815.94 | 0.661 |  |
| cluster_embeddings_agglomerative | clustered_5clusters - agglomerative | success | 6.164 | 23.14 | 845.47 | 0.642 |  |
| cluster_embeddings_kmeans | clustered_10clusters - kmeans | success | 14.850 | 0.06 | 846.00 | 0.137 |  |
| cluster_embeddings_dbscan | clustered_10clusters - dbscan | success | 6.277 | 0.12 | 851.92 | 0.648 |  |
| cluster_embeddings_agglomerative | clustered_10clusters - agglomerative | success | 6.183 | 0.36 | 851.23 | 0.674 |  |
| detect_lewd_images | - | success | 9.632 | -140.19 | 1748.17 | 1.792 |  |
| detect_lewd_images | - | success | 9.470 | -15.81 | 1820.66 | 1.739 |  |
| detect_lewd_images | - | success | 9.424 | -114.45 | 1905.08 | 1.773 |  |
| detect_lewd_images | - | success | 9.016 | 14.83 | 1871.75 | 1.759 |  |
| detect_lewd_images | - | success | 8.182 | -114.05 | 1798.22 | 2.125 |  |
| detect_lewd_images | - | success | 9.196 | 58.14 | 1863.23 | 1.753 |  |
| detect_lewd_images | - | success | 8.842 | 47.11 | 1881.09 | 1.772 |  |
| detect_lewd_images | - | success | 8.761 | 53.41 | 1892.48 | 1.787 |  |
| detect_lewd_images | - | success | 9.087 | -21.03 | 1848.25 | 1.734 |  |
| detect_lewd_images | - | success | 6.579 | 53.12 | 1865.45 | 1.780 |  |
| detect_lewd_images | - | success | 9.302 | -24.25 | 1877.45 | 1.800 |  |
| detect_text_in_image | - | success | 12.963 | 5.95 | 1615.22 | 0.068 |  |
| detect_text_in_image | - | success | 10.756 | 0.03 | 1615.25 | 0.063 |  |
| detect_text_in_image | - | success | 15.024 | 0.00 | 1615.25 | 0.062 |  |
| detect_text_in_image | - | success | 11.240 | 0.00 | 1615.25 | 0.080 |  |
| detect_text_in_image | - | success | 6.466 | 0.00 | 1615.25 | 0.060 |  |
| detect_text_in_image | - | success | 8.662 | 0.00 | 1615.25 | 0.054 |  |
| detect_text_in_image | - | success | 8.693 | 0.00 | 1615.25 | 0.053 |  |
| detect_text_in_image | - | success | 6.450 | 0.00 | 1615.25 | 0.101 |  |
| detect_text_in_image | - | success | 5.869 | 0.00 | 1615.25 | 0.059 |  |
| detect_text_in_image | - | success | 8.997 | 0.00 | 1615.25 | 0.093 |  |
| detect_text_in_image | - | success | 8.067 | 0.00 | 1615.25 | 0.055 |  |
| dimension_reduction_tsne | small_500x512 - tsne | success | 6.242 | 5.47 | 1679.20 | 8.336 |  |
| dimension_reduction_umap | small_500x512 - umap | success | 8.190 | 10.77 | 1689.98 | 2.457 |  |
| dimension_reduction_tsne | medium_2000x512 - tsne | success | 16.433 | 22.95 | 1712.94 | 85.710 |  |
| dimension_reduction_umap | medium_2000x512 - umap | success | 10.407 | 30.62 | 1745.19 | 2.752 |  |
| dimension_reduction_tsne | large_5000x512 - tsne | success | 35.137 | 64.00 | 1829.20 | 282.059 |  |
| dimension_reduction_umap | large_5000x512 - umap | success | 16.055 | 14.64 | 1873.23 | 8.524 |  |
| dimension_reduction_tsne | xlarge_10000x512 - tsne | success | 63.125 | 68.48 | 2008.08 | 537.380 |  |
| dimension_reduction_umap | xlarge_10000x512 - umap | success | 14.706 | 19.53 | 2041.16 | 9.226 |  |
