"""Operator to perform dimensionality reduction given the embedddings."""

from abc import ABC, abstractmethod
from sklearn.manifold import TSNE
import numpy as np


class DimensionReduction(ABC):
    """Abstract base class for dimension reduction techniques."""

    @abstractmethod
    def initialize(self, params):
        pass

    @abstractmethod
    def run(self, embeddings):
        pass


class TSNEReduction(DimensionReduction):
    """t-SNE implementation of the DimensionReduction abstract class."""

    def initialize(self, params):
        """
        Initialize the t-SNE model with parameters.

        Args:
            params (dict): A dictionary containing t-SNE parameters such as:
                - n_components (int): Number of dimensions to reduce to. Default is 2.
                - perplexity (float): Perplexity parameter for t-SNE. Default is 30.
                - learning_rate (float): Learning rate for t-SNE. Default is 150.
                - n_iter (int): Number of iterations for optimization. Default is 1000.
                - random_state (int): Seed for random number generation. Default is 42.
                - method (str): Algorithm to use for gradient calculation. Default is barnes_hut

        Raises:
            ValueError: If the t-SNE model fails to initialize.
        """
        try:
            self.model = TSNE(
                n_components=params.get('n_components', 2),
                perplexity=params.get('perplexity', 30),
                learning_rate=params.get('learning_rate', 150),
                max_iter=params.get('max_iter', 1000),
                random_state=params.get('random_state', 42),
                method=params.get('method', 'barnes_hut')
            )
            print("t-SNE model successfully initialized")
        except Exception as e:
            raise ValueError(f"Failed to initialize t-SNE model: {e}")

    def run(self, embeddings_array):
        """
        Apply the t-SNE model to reduce the dimensionality of embeddings.

        Args:
            embeddings (list or numpy.ndarray): A list or array of embeddings to be reduced.

        Returns:
            numpy.ndarray: The reduced embeddings as a 2D array.

        Raises:
            ValueError: If the embeddings input is not a 2D array.
            RuntimeError: If the t-SNE reduction fails.
        """
        try:
            if embeddings_array.ndim != 2:
                raise ValueError("Embeddings should be a 2D array.")
            return self.model.fit_transform(embeddings_array)
        except Exception as e:
            raise RuntimeError(f"t-SNE reduction failed: {e}")


class DimensionReductionFactory:
    """Factory class for creating dimension reduction models."""

    @staticmethod
    def get_reduction_model(model_type):
        """
        Factory method to create a dimension reduction model based on type.

        Args:
            model_type (str): String indicating the type of model (e.g., 'tsne').

        Returns:
            DimensionReduction: An instance of the corresponding dimension reduction model.

        Raises:
            ValueError: If the specified model type is unsupported.
        """
        if model_type.lower() == 'tsne':
            return TSNEReduction()
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


def gen_data(payloads, reduced_embeddings):
    """
    Generates the formatted output.

    Args:
        payloads (list): List of paylods.
        reduced_embeddings (nd.array): An array of reduced embeddings.

    Returns:
        list: A list of dictionaries containing the payload and corresponding embedding.
    """
    out = []

    for payload, reduced_embedding in zip(payloads, reduced_embeddings):
        tmp_dict = {}
        tmp_dict['payload'] = payload
        tmp_dict['reduced_embedding'] = reduced_embedding.tolist()
        out.append(tmp_dict)
    return out


def initialize(params):
    """
    Initialize the dimension reduction model with provided type and parameters.

    Args:
        params (dict): Dictionary of parameters for the model initialization.

    """
    global reduction_model
    reduction_model = DimensionReductionFactory.get_reduction_model(params.get('model_type', 'tsne'))
    reduction_model.initialize(params)


def run(input_data):
    """
    Reduce the dimensionality of the provided embeddings using the initialized model.

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
        embeddings, payloads = zip(*[(data['embedding'], data['payload']) for data in input_data])
    except KeyError as e:
        raise KeyError(f"Invalid data. Each data point in input must have `embedding` and `payload` properties. Missing key: {e}.")
    
    reduced_embeddings = reduction_model.run(np.array(embeddings))

    return gen_data(payloads, reduced_embeddings)