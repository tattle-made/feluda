"""
Operator to cluster embeddings using KMeans, Affinity Propagation, and Agglomerative clustering algorithms
"""

def initialize(param):
    """
    Initializes the operator.

    Args:
        param (dict): Parameters for initialization
    """
    global KMeans_clustering, Agglomerative_clustering, AffinityPropagation_clustering
    global gen_data

    # Imports
    from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering
    import numpy as np

    # Constants
    RANDOM_STATE = 50

    def gen_data(labels, input_data):
        """
        Generates formatted output data.

        Args:
            labels (np.ndarray): An array of cluster labels
            input_data (list[dict]): Operator input

        Returns:
            dict: A dictionary mapping cluster labels to corresponding array of payloads
        """
        out = {}
        for label, item in zip(labels, input_data):
            key = f'cluster_{label}'
            if key not in out:
                out[key] = []
            out[key].append(item['payload'])
        return out

    def KMeans_clustering(matrix, n_clusters):
        """
        Clusters given embeddings using KMeans clustering algorithm.

        Args:
            matrix (list[list]): list of embeddings
            n_clusters (int): number of clusters

        Returns:
            numpy.ndarray: An array of cluster labels for each embedding
        """
        return KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE).fit_predict(np.array(matrix))

    def Agglomerative_clustering(matrix, n_clusters):
        """
        Clusters given embeddings using Agglomerative clustering algorithm.

        Args:
            matrix (list[list]): list of embeddings
            n_clusters (int): number of clusters

        Returns:
            numpy.ndarray: An array of cluster labels for each embedding
        """
        return AgglomerativeClustering(n_clusters=n_clusters).fit_predict(np.array(matrix))

    def AffinityPropagation_clustering(matrix):
        """
        Clusters given embeddings using Affinity Propagation algorithm (used if the number of clusters is unknown).

        Args:
            matrix (list[list]): list of embeddings

        Returns:
            numpy.ndarray: An array of cluster labels for each embedding
        """
        return AffinityPropagation(random_state=RANDOM_STATE).fit_predict(np.array(matrix))

def run(embeddings, n_clusters=None, modality='audio'):
    """
    Runs the operator.

    Args:
        embeddings (list[dict]): List of data with each dictionary containing `embedding` and `payload` properties
        n_clusters (int, optional): Number of clusters. Defaults to None
        modality (str, optional): Source modality of embeddings. Defaults to 'audio'

    Returns:
        dict: A dictionary mapping cluster labels to corresponding array of payloads

    Raises:
        ValueError: If invalid modality is provided
    """
    matrix = [data['embedding'] for data in embeddings] # isolating list of embeddings
    if n_clusters:
        if modality == 'audio':
            labels = KMeans_clustering(matrix=matrix, n_clusters=n_clusters)
        elif modality == 'visual':
            labels = Agglomerative_clustering(matrix=matrix, n_clusters=n_clusters)
        else:
            raise ValueError("Invalid modality. Modality can only be `audio` or `visual`.")
    else:
        labels = AffinityPropagation_clustering(matrix=matrix)
    return gen_data(labels=labels, input_data=embeddings)
