"""
Operator to cluster embeddings using KMeans, Affinity Propagation, and Agglomerative clustering algorithms
"""

def initialize(param):
    """
    Initializes the operator.

    Args:
        param (dict): Parameters for initialization
    """
    # Move logging configuration inside initialize()
    import logging
    logging.basicConfig(level=logging.INFO)

    # Constants
    global RANDOM_STATE, BATCH_SIZE
    RANDOM_STATE = 50
    BATCH_SIZE = 1000  # Batch size for large datasets

    logging.info("Initializing clustering operator with parameters: %s", param)

    # Import libraries inside initialize()
    import numpy as np
    from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, KMeans

    # Define functions inside initialize()
    global gen_data, batch_process
    global KMeans_clustering, Agglomerative_clustering, AffinityPropagation_clustering

    def gen_data(payloads, labels):
        """
        Generates formatted output data.

        Args:
            payloads (list): List of payloads
            labels (np.ndarray): An array of cluster labels

        Returns:
            dict: A dictionary mapping cluster labels to corresponding array of payloads
        """
        out = {}
        for label, payload in zip(labels, payloads):
            key = f"cluster_{label}"
            if key not in out:
                out[key] = []
            out[key].append(payload)
        return out

    def batch_process(matrix, batch_size, cluster_func, **kwargs):
        """
        Batch processes the clustering algorithm to handle large datasets.

        Args:
            matrix (list[list]): List of embeddings
            batch_size (int): Size of each batch
            cluster_func (function): Clustering function to use
            **kwargs: Additional arguments for the clustering function

        Returns:
            np.ndarray: Concatenated cluster labels from all batches
        """
        num_batches = (len(matrix) + batch_size - 1) // batch_size
        labels = []

        for i in range(num_batches):
            start = i * batch_size
            end = min((i + 1) * batch_size, len(matrix))

            logging.info(f"Processing batch {i + 1}/{num_batches}...")

            batch = np.array(matrix[start:end])
            batch_labels = cluster_func(batch, **kwargs)
            labels.extend(batch_labels)

        return np.array(labels)

    def KMeans_clustering(matrix, n_clusters):
        """
        Clusters given embeddings using KMeans clustering algorithm.

        Args:
            matrix (np.ndarray): 2D array of embeddings
            n_clusters (int): Number of clusters

        Returns:
            np.ndarray: Cluster labels
        """
        try:
            return KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE).fit_predict(matrix)
        except Exception as e:
            logging.error(f"KMeans clustering failed: {e}")
            raise RuntimeError(f"KMeans clustering failed: {e}")

    def Agglomerative_clustering(matrix, n_clusters):
        """
        Clusters given embeddings using Agglomerative clustering algorithm.

        Args:
            matrix (np.ndarray): 2D array of embeddings
            n_clusters (int): Number of clusters

        Returns:
            np.ndarray: Cluster labels
        """
        try:
            return AgglomerativeClustering(n_clusters=n_clusters).fit_predict(matrix)
        except Exception as e:
            logging.error(f"Agglomerative clustering failed: {e}")
            raise RuntimeError(f"Agglomerative clustering failed: {e}")

    def AffinityPropagation_clustering(matrix):
        """
        Clusters given embeddings using Affinity Propagation algorithm.

        Args:
            matrix (np.ndarray): 2D array of embeddings

        Returns:
            np.ndarray: Cluster labels
        """
        try:
            return AffinityPropagation(random_state=RANDOM_STATE).fit_predict(matrix)
        except Exception as e:
            logging.error(f"Affinity Propagation clustering failed: {e}")
            raise RuntimeError(f"Affinity Propagation clustering failed: {e}")


def run(input_data, n_clusters=None, modality="audio"):
    """
    Runs the clustering operator.

    Args:
        input_data (list[dict]): List of data with `embedding` and `payload`
        n_clusters (int, optional): Number of clusters. Defaults to None
        modality (str, optional): Source modality. Defaults to 'audio'

    Returns:
        dict: Cluster labels mapped to payloads
    """
    import logging

    import numpy as np
    logging.info(f"Running clustering with {modality} modality and {n_clusters} clusters")

    # Validate input data
    if not isinstance(input_data, list) or len(input_data) == 0:
        raise ValueError("Input data should be a non-empty list of dictionaries.")

    # Extract matrix and payloads
    try:
        matrix, payloads = zip(
            *[(data["embedding"], data["payload"]) for data in input_data]
        )
        matrix = np.array(matrix)
    except KeyError as e:
        raise KeyError(f"Missing key: {e} in input data.")

    # Select clustering algorithm
    if n_clusters:
        cluster_func = KMeans_clustering if modality == "audio" else Agglomerative_clustering
        labels = batch_process(matrix, BATCH_SIZE, cluster_func, n_clusters=n_clusters)
    else:
        labels = batch_process(matrix, BATCH_SIZE, AffinityPropagation_clustering)

    # Generate formatted output
    output = gen_data(payloads=payloads, labels=labels)

    logging.info("Clustering completed successfully.")
    return output


def cleanup(param):
    """
    Cleans up resources after execution.
    """
    import logging
    logging.info("Cleaning up resources...")
    import gc
    gc.collect()


def state():
    """
    Returns the current state of the operator.

    Returns:
        dict: Current state information
    """
    import logging
    logging.info("Fetching operator state...")
    return {"status": "ready"}
