import gc
from dataclasses import dataclass
from typing import Any

import numpy as np
import umap
from sklearn.manifold import TSNE

from feluda import Operator


class ReductionModel:
    """Base class for dimension reduction models."""

    def __init__(self, params: Any) -> None:
        self.params = params

    @staticmethod
    def validate_embeddings(embeddings_array: np.ndarray) -> np.ndarray:
        """Validate embeddings array, converting list to numpy array if needed.

        Args:
            embeddings_array: Either a list or numpy array of embeddings


        Raises:
            ValueError: If the embeddings are invalid
        """
        if not isinstance(embeddings_array, np.ndarray):
            raise ValueError("Embeddings must be a list or numpy array")

        if embeddings_array.ndim != 2:
            raise ValueError("Embeddings should be a 2D array")

        if embeddings_array.shape[0] == 0 or embeddings_array.shape[1] == 0:
            raise ValueError("Embeddings array cannot be empty or have zero dimensions")

        if not np.issubdtype(embeddings_array.dtype, np.number):
            raise ValueError("Embeddings must contain numeric values")

        if np.any(np.isnan(embeddings_array)) or np.any(np.isinf(embeddings_array)):
            raise ValueError("Embeddings contain NaN or infinite values")


@dataclass
class TSNEParams:
    """Configuration parameters for t-SNE dimensionality reduction.

    Attributes:
        n_components: Number of dimensions to reduce to (default: 2)
        perplexity: Perplexity parameter for t-SNE (default: 30.0)
        learning_rate: Learning rate for optimization (default: 150.0)
        max_iter: Maximum number of iterations (default: 1000)
        random_state: Random seed for reproducibility (default: 42)
        method: Algorithm method ('barnes_hut' or 'exact') (default: 'barnes_hut')
    """

    n_components: int = 2
    perplexity: float = 30.0
    learning_rate: float = 150.0
    max_iter: int = 1000
    random_state: int = 42
    method: str = "barnes_hut"

    def __post_init__(self) -> None:
        """Validate t-SNE parameters."""
        if self.n_components < 1:
            raise ValueError("n_components must be at least 1")
        if self.perplexity <= 0:
            raise ValueError("perplexity must be positive")
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")
        if self.max_iter < 1:
            raise ValueError("max_iter must be at least 1")
        if self.method not in {"barnes_hut", "exact"}:
            raise ValueError("method must be 'barnes_hut' or 'exact'")


@dataclass
class UMAPParams:
    """Configuration parameters for UMAP dimensionality reduction.

    Attributes:
        n_components: Number of dimensions to reduce to (default: 2)
        n_neighbors: Size of local neighborhood (default: 15)
        min_dist: Minimum distance between embedded points (default: 0.1)
        metric: Distance metric to use (default: 'euclidean')
        random_state: Random seed for reproducibility (default: 42)
    """

    n_components: int = 2
    n_neighbors: int = 15
    min_dist: float = 0.1
    metric: str = "euclidean"
    random_state: int = 42

    def __post_init__(self) -> None:
        """Validate UMAP parameters."""
        if self.n_components < 1:
            raise ValueError("n_components must be at least 1")
        if self.n_neighbors < 2:
            raise ValueError("n_neighbors must be at least 2")
        if not (0 <= self.min_dist <= 1):
            raise ValueError("min_dist must be between 0 and 1")


class TSNEReduction(ReductionModel):
    """T-SNE (t-Distributed Stochastic Neighbor Embedding) dimension
    reduction.
    """

    def __init__(self, params: TSNEParams) -> None:
        """Initialize the t-SNE model with parameters.

        Args:
            params: TSNE configuration parameters

        Raises:
            ValueError: If the t-SNE model fails to initialize
        """
        super().__init__(params)
        try:
            self.model = TSNE(
                n_components=params.n_components,
                perplexity=params.perplexity,
                learning_rate=params.learning_rate,
                max_iter=params.max_iter,
                random_state=params.random_state,
                method=params.method,
            )
            print("t-SNE model successfully initialized")
        except Exception as e:
            raise ValueError(f"Failed to initialize t-SNE model: {e}")

    def run(self, embeddings_array: np.ndarray) -> np.ndarray:
        """Apply the t-SNE model to reduce the dimensionality of embeddings.

        Args:
            embeddings_array: A 2D numpy array of embeddings to be reduced

        Returns:
            numpy.ndarray: The reduced embeddings as a 2D array.
        """
        self.validate_embeddings(embeddings_array)
        try:
            return self.model.fit_transform(embeddings_array)
        except Exception as e:
            raise RuntimeError(f"t-SNE reduction failed: {e}")


class UMAPReduction(ReductionModel):
    """UMAP (Uniform Manifold Approximation and Projection) dimension
    reduction.
    """

    def __init__(self, params: UMAPParams) -> None:
        """Initialize the UMAP model with parameters.

        Args:
            params: UMAP configuration parameters

        Raises:
            ValueError: If the UMAP model fails to initialize
        """
        super().__init__(params)
        try:
            self.model = umap.UMAP(
                n_components=params.n_components,
                n_neighbors=params.n_neighbors,
                min_dist=params.min_dist,
                metric=params.metric,
                random_state=params.random_state,
            )
            print("UMAP model successfully initialized")
        except Exception as e:
            raise ValueError(f"Failed to initialize UMAP model: {e}")

    def run(self, embeddings_array: np.ndarray) -> np.ndarray:
        """Apply the UMAP model to reduce the dimensionality of embeddings.

        Args:
            embeddings_array: A 2D numpy array of embeddings to be reduced

        Returns:
            numpy.ndarray: The reduced embeddings as a 2D array.
        """
        self.validate_embeddings(embeddings_array)
        try:
            return self.model.fit_transform(embeddings_array)
        except Exception as e:
            raise RuntimeError(f"UMAP reduction failed: {e}")


class DimensionReduction(Operator):
    """Main interface for dimensionality reduction."""

    def __init__(self, model_type: str, params: dict[str, Any] | None = None) -> None:
        """Initialize the dimension reduction operator.

        Args:
            model_type: Type of model to use ('tsne' or 'umap')
            params: Optional dictionary of parameters for the model

        Raises:
            ValueError: If the model type is not supported or initialization fails
        """
        if params is None:
            params = {}

        try:
            self.reduction_model: ReductionModel = self.get_reduction_model(
                model_type, params
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize dimension reduction model: {e}")

    @staticmethod
    def get_reduction_model(model_type: str, params: dict[str, Any]) -> ReductionModel:
        """Create a dimension reduction model based on the model type.

        Args:
            model_type: Type of model ('tsne' or 'umap')
            params: Dictionary of parameters for the model

        Returns:
            A dimension reduction model instance
        """
        model_type_lower = model_type.lower()

        if model_type_lower == "tsne":
            tsne_params = TSNEParams(**params)
            return TSNEReduction(tsne_params)
        if model_type_lower == "umap":
            umap_params = UMAPParams(**params)
            return UMAPReduction(umap_params)
        raise ValueError(f"Unsupported model type: {model_type}")

    @staticmethod
    def gen_data(payloads: list, reduced_embeddings: np.ndarray) -> list[dict]:
        """Generates the formatted output.

        Args:
            payloads (list): List of paylods.
            reduced_embeddings (nd.array): An array of reduced embeddings.

        Returns:
            list: A list of dictionaries containing the payload and corresponding embedding.
        """
        return [
            {
                "payload": payload,
                "reduced_embedding": reduced_embedding.tolist(),
            }
            for payload, reduced_embedding in zip(
                payloads, reduced_embeddings, strict=False
            )
        ]

    def run(self, input_data: list[dict]) -> list[dict]:
        """Reduce the dimensionality of the provided embeddings using the
        initialized model.

        Args:
            input_data (list): A list of dictionaries containing payload and embeddings to be reduced.

        Example:
            [
                {
                    "payload": "123",
                    "embedding": [1, 2, 3]
                },
                {
                    "payload": "124",
                    "embedding": [1, 0, 1]
                }
            ]

        Returns:
            list: The reduced embeddings and the corresponding payload as a list of dictionaries.

        Example:
            [
                {
                    "payload":"123",
                    "reduced_embedding": [1, 2]
                },
                {
                    "payload": "124",
                    "reduced_embedding": [1, 0]
                }
            ]

        Raises:
            ValueError: If the embeddings input is not a non-empty list.
            KeyError: If the input data is invalid.
        """
        if not isinstance(input_data, list) or len(input_data) == 0:
            raise ValueError("Input should be a non-empty list.")

        try:
            self.embeddings, self.payloads = zip(
                *[(data["embedding"], data["payload"]) for data in input_data],
                strict=False,
            )
        except KeyError as e:
            raise KeyError(f"Missing key in input data: {e}")

        self.embeddings = np.array(self.embeddings)

        self.reduced = self.reduction_model.run(self.embeddings)
        return self.gen_data(self.payloads, self.reduced)

    def cleanup(self) -> None:
        """Cleans up resources used by the operator."""
        del self.reduction_model
        self.embeddings = None
        self.payloads = None
        self.reduced = None
        self.reduction_model = None

        gc.collect()

    def state(self) -> dict:
        """Returns the current state of the operator.

        Returns:
            dict: State of the operator
        """
        if not hasattr(self, "reduction_model"):
            raise RuntimeError("Reduction model is not initialized.")
        return {
            "model": self.reduction_model,
            "embeddings": self.embeddings.tolist(),
            "payloads": self.payloads,
            "reduced": self.reduced.tolist(),
        }
