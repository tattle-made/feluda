import os
from typing import Any

import numpy as np
from PIL import Image


class DataGenerator:
    """Generate synthetic datasets for benchmarking operators."""

    # -----------------------
    # Embedding Generation
    # -----------------------
    @staticmethod
    def generate_embeddings(num_samples: int, dim: int = 512) -> np.ndarray:
        """
        Generate random embeddings for testing.

        Args:
            num_samples: Number of embedding vectors.
            dim: Dimension of each vector (default 512 for CLIP).

        Returns:
            NumPy array of shape (num_samples, dim) with float32 values.
        """
        return np.random.randn(num_samples, dim).astype(np.float32)

    @staticmethod
    def generate_embeddings_with_clusters(
        num_clusters: int = 5,
        samples_per_cluster: int = 100,
        dim: int = 512,
        cluster_spread: float = 0.3,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Generate embeddings with a known cluster structure.

        Args:
            num_clusters: Number of clusters.
            samples_per_cluster: Samples per cluster.
            dim: Embedding dimension.
            cluster_spread: Standard deviation within clusters.

        Returns:
            (embeddings, labels)
        """
        centers = np.random.randn(num_clusters, dim) * 3
        embeddings = []
        labels = []

        for i, center in enumerate(centers):
            points = center + np.random.randn(samples_per_cluster, dim) * cluster_spread
            embeddings.append(points)
            labels.extend([i] * samples_per_cluster)

        embeddings = np.vstack(embeddings).astype(np.float32)
        labels = np.array(labels)

        indices = np.random.permutation(len(embeddings))
        return embeddings[indices], labels[indices]

    # -----------------------
    # Image Generation
    # -----------------------
    @staticmethod
    def generate_test_images(output_dir: str) -> list[dict[str, Any]]:
        """
        Generate test images in various resolutions and modes.

        Args:
            output_dir: Directory to save generated images.

        Returns:
            List of dictionaries containing image metadata.
        """
        os.makedirs(output_dir, exist_ok=True)

        image_configs = [
            # Small
            {"size": (128, 128), "mode": "RGB", "name": "small_128x128.jpg"},
            {"size": (256, 256), "mode": "RGB", "name": "small_256x256.jpg"},
            {"size": (320, 240), "mode": "RGB", "name": "small_320x240.jpg"},
            # Medium
            {"size": (640, 480), "mode": "RGB", "name": "medium_640x480.jpg"},
            {"size": (800, 600), "mode": "RGB", "name": "medium_800x600.jpg"},
            {"size": (1024, 768), "mode": "RGB", "name": "medium_1024x768.jpg"},
            # HD
            {"size": (1280, 720), "mode": "RGB", "name": "hd_1280x720.jpg"},
            {"size": (1920, 1080), "mode": "RGB", "name": "fullhd_1920x1080.jpg"},
            # 4K
            {"size": (3840, 2160), "mode": "RGB", "name": "4k_3840x2160.jpg"},
            {"size": (4096, 2160), "mode": "RGB", "name": "cinema4k_4096x2160.jpg"},
            # Grayscale
            {"size": (512, 512), "mode": "L", "name": "gray_512x512.jpg"},
            {"size": (1024, 1024), "mode": "L", "name": "gray_1024x1024.jpg"},
            # Aspect ratio variations
            {"size": (1920, 480), "mode": "RGB", "name": "wide_1920x480.jpg"},
            {"size": (480, 1920), "mode": "RGB", "name": "tall_480x1920.jpg"},
            {"size": (2048, 2048), "mode": "RGB", "name": "square_2048x2048.jpg"},
        ]

        generated_images = []
        for cfg in image_configs:
            arr_shape = (
                (*cfg["size"][::-1], 3) if cfg["mode"] == "RGB" else cfg["size"][::-1]
            )
            arr = np.random.randint(0, 256, arr_shape, dtype=np.uint8)
            img = Image.fromarray(arr, mode=cfg["mode"])

            filepath = os.path.join(output_dir, cfg["name"])
            img.save(filepath, quality=95)
            file_size = os.path.getsize(filepath)

            generated_images.append({
                "name": cfg["name"],
                "path": filepath,
                "width": cfg["size"][0],
                "height": cfg["size"][1],
                "mode": cfg["mode"],
                "file_size_bytes": file_size,
                "file_size_mb": file_size / (1024 * 1024),
            })

        return generated_images

    # -----------------------
    # Prebuilt Dataset Collections
    # -----------------------
    @staticmethod
    def generate_embedding_datasets() -> dict[str, np.ndarray]:
        """
        Generate a collection of embedding datasets of varying sizes and shapes.

        Returns:
            Dict mapping dataset name to NumPy array.
        """
        datasets = {
            # Small
            "tiny_100x512": DataGenerator.generate_embeddings(100, 512),
            "small_500x512": DataGenerator.generate_embeddings(500, 512),
            "small_1000x512": DataGenerator.generate_embeddings(1000, 512),
            # Medium
            "medium_5000x512": DataGenerator.generate_embeddings(5000, 512),
            "medium_10000x512": DataGenerator.generate_embeddings(10000, 512),
            # Large
            "large_25000x512": DataGenerator.generate_embeddings(25000, 512),
            "large_50000x512": DataGenerator.generate_embeddings(50000, 512),
            # Different dimensions
            "small_1000x256": DataGenerator.generate_embeddings(1000, 256),
            "small_1000x1024": DataGenerator.generate_embeddings(1000, 1024),
            "small_1000x2048": DataGenerator.generate_embeddings(1000, 2048),
            # Very large
            "xlarge_100000x512": DataGenerator.generate_embeddings(100000, 512),
        }

        # Add clustered datasets
        for n_clusters in [3, 5, 10, 20]:
            embeddings, _ = DataGenerator.generate_embeddings_with_clusters(
                num_clusters=n_clusters, samples_per_cluster=200, dim=512
            )
            datasets[f"clustered_{n_clusters}clusters_x512"] = embeddings
        return datasets
