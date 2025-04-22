import os
import tempfile
import unittest

import yaml

from feluda import Feluda
from feluda.models.media_factory import AudioFactory


class TestFeludaClusterEmbeddingsIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        cls.config = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "Cluster Embeddings",
                        "type": "cluster_embeddings",
                        "parameters": {"index_name": "audio"},
                    }
                ],
            }
        }

        # Create a temporary configuration file
        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        # Initialize Feluda
        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()

        cls.test_audio_url = "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/audio.wav"

    def test_cluster_embeddings(self):
        """Test the cluster_embeddings operator."""
        audio_obj = AudioFactory.make_from_url(self.test_audio_url)
        self.assertIsNotNone(audio_obj, "Audio object should be successfully created")

        print(f"Audio object: {audio_obj}")

        # Generate mock embeddings and payloads for testing
        embedding_1 = [0.1, 0.2, 0.3]  # Mock embedding for sample 1
        embedding_2 = [0.4, 0.5, 0.6]  # Mock embedding for sample 2
        payload_1 = {"path": audio_obj["path"]}
        payload_2 = {"path": audio_obj["path"]}

        # Prepare input_data with at least 2 samples
        input_data = [
            {"embedding": embedding_1, "payload": payload_1},
            {"embedding": embedding_2, "payload": payload_2},
        ]

        operator = self.feluda.operators.get()["cluster_embeddings"]
        result = operator.run(input_data=input_data, n_clusters=2, modality="audio")

        self.assertIn("cluster_0", result)
        self.assertIn("cluster_1", result)
        self.assertEqual(len(result), 2)

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files."""
        try:
            os.remove(cls.config_path)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
