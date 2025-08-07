import numpy as np
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, KMeans

from feluda import Operator

RANDOM_STATE = 50


class ClusterEmbeddings(Operator):
    """Operator to cluster embeddings using KMeans, Affinity Propagation, and
    Agglomerative clustering algorithms.
    """

    def __init__(self) -> None:
        """Initialize the `ClusterEmbeddings` operator."""
        super().__init__()
        self.matrix = []
        self.payloads = []
        self.modality = None
        self.n_clusters = None

    @staticmethod
    def gen_data(payloads: list[dict], labels: np.ndarray) -> dict:
        """Generate formatted output data.

        Args:
            payloads (list): List of payloads
            labels (np.ndarray): An array of cluster labels

        Returns:
            dict: A dictionary mapping cluster labels to corresponding array of payloads
        """
        out = {}
        for label, payload in zip(labels, payloads, strict=False):
            key = f"cluster_{label}"
            if key not in out:
                out[key] = []
            out[key].append(payload)
        return out

    @staticmethod
    def kmeans(matrix: list[list], n_clusters: int) -> np.ndarray:
        """Cluster embeddings using KMeans.

        Args:
            matrix (list[list]): list of embeddings
            n_clusters (int): number of clusters

        Returns:
            numpy.ndarray: An array of cluster labels for each embedding
        """
        return KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE).fit_predict(
            np.array(matrix)
        )

    @staticmethod
    def agglomerative(matrix: list[list], n_clusters: int) -> np.ndarray:
        """Cluster embeddings using Agglomerative Clustering.

        Args:
            matrix (list[list]): list of embeddings
            n_clusters (int): number of clusters

        Returns:
            numpy.ndarray: An array of cluster labels for each embedding
        """
        return AgglomerativeClustering(n_clusters=n_clusters).fit_predict(
            np.array(matrix)
        )

    @staticmethod
    def affinity_propagation(matrix: list[list]) -> np.ndarray:
        """Cluster embeddings using Affinity Propagation.

        (Used if the number of clusters is unknown).

        Args:
            matrix (list[list]): list of embeddings

        Returns:
            numpy.ndarray: An array of cluster labels for each embedding
        """
        return AffinityPropagation(random_state=RANDOM_STATE).fit_predict(
            np.array(matrix)
        )

    def run(
        self, input_data: list[dict], n_clusters: int = None, modality: str = None
    ) -> dict:
        """Run the operator.

        Args:
            input_data (list[dict]): List of data with each dictionary containing `embedding` and `payload` properties
            n_clusters (int, optional): Number of clusters. Defaults to None
            modality (str, optional): Source modality of embeddings. Defaults to None

        Returns:
            dict: A dictionary mapping cluster labels to corresponding array of payloads
        """
        if modality not in {"audio", "video"}:
            raise ValueError(
                "Modality must be specified and should be either `audio` or `video`."
            )
        self.modality = modality

        if not isinstance(input_data, list) or not input_data:
            raise ValueError("input_data must be a non-empty list of dicts.")

        # Parse data:
        try:
            self.matrix, self.payloads = zip(
                *[(data["embedding"], data["payload"]) for data in input_data],
                strict=False,
            )
        except KeyError as e:
            raise KeyError(
                f"Invalid data. Each data point in input must have `embedding` and `payload` properties. Missing key: {e}."
            )

        # Delegate appropriate clustering algorithm for the given params:
        if n_clusters:
            self.n_clusters = int(n_clusters)  # cast it to int
            if modality == "audio":
                labels = self.kmeans(self.matrix, self.n_clusters)
            elif modality == "video":
                labels = self.agglomerative(self.matrix, self.n_clusters)
            else:
                raise ValueError(
                    "Invalid modality. Modality should be either `audio` or `video`."
                )
        else:
            labels = self.affinity_propagation(self.matrix)
        return self.gen_data(payloads=self.payloads, labels=labels)

    def cleanup(self) -> None:
        """Clean up resources used by the operator."""
        self.matrix = []
        self.payloads = []
        self.modality = None
        self.n_clusters = None

    def state(self) -> dict:
        """Return the current state of the operator.

        Returns:
            dict: State of the operator
        """
        return {
            "modality": self.modality,
            "n_clusters": self.n_clusters,
            "matrix": [list(row) for row in self.matrix],
            "payloads": self.payloads,
        }
