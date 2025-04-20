import os
import tempfile
import unittest
from pathlib import Path

import numpy as np
import yaml

from feluda import Feluda
from feluda.models.media_factory import VideoFactory


class TestFeludaVideoVectorIntegration(unittest.TestCase):
    config_path = None
    feluda = None

    @classmethod
    def setUpClass(cls):
        cls.config = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "video vector",
                        "type": "vid_vec_rep_clip",
                        "parameters": {"index_name": "video"},
                    }
                ],
            }
        }

        fd, cls.config_path = tempfile.mkstemp(suffix=".yml", text=True)
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        try:
            cls.feluda = Feluda(cls.config_path)
            cls.feluda.setup()
        except Exception as e:
            if cls.config_path and Path(cls.config_path).exists():
                Path(cls.config_path).unlink()
            raise RuntimeError(f"Feluda setup failed: {e}") from e

        cls.test_video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"
        cls.expected_vector_dim = 512

    def setUp(self):
        self.operator = self.feluda.operators.get()["vid_vec_rep_clip"]
        if not self.operator:
            self.fail("Failed to get operator 'vid_vec_rep_clip' from Feluda instance")

    def test_video_vector_generation(self):
        video_object = VideoFactory.make_from_url(self.test_video_url)
        downloaded_path = video_object.get("path")
        self.assertIsNotNone(downloaded_path, "VideoFactory did not return a path")
        self.assertTrue(
            Path(downloaded_path).exists(),
            f"Downloaded file not found at {downloaded_path}",
        )

        vector_generator = self.operator.run(video_object)

        try:
            first_output_item = next(vector_generator)
        except Exception as e:
            if Path(downloaded_path).exists():
                os.remove(downloaded_path)
            self.fail(f"Calling next on generator raised an unexpected error: {e}")

        self.assertIsInstance(
            first_output_item, dict, "Operator did not yield a dictionary"
        )
        self.assertIn(
            "vid_vec", first_output_item, "Yielded dictionary missing 'vid_vec' key"
        )
        self.assertIn(
            "is_avg", first_output_item, "Yielded dictionary missing 'is_avg' key"
        )

        actual_vector = first_output_item["vid_vec"]
        is_average = first_output_item["is_avg"]

        self.assertTrue(is_average, "First yielded vector should have is_avg=True")

        self.assertIsInstance(
            actual_vector, list, "Vector ('vid_vec') should be a list"
        )
        self.assertTrue(len(actual_vector) > 0, "Vector should not be empty")
        self.assertEqual(
            len(actual_vector),
            self.expected_vector_dim,
            f"Vector should have dimension {self.expected_vector_dim}",
        )

        vector_np = np.array(actual_vector)
        self.assertFalse(np.all(vector_np == 0), "Vector should not be all zeros")
        self.assertFalse(
            np.any(np.isnan(vector_np)), "Vector should not contain NaN values"
        )

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests are done."""
        try:
            Path(cls.config_path).unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: Failed to delete temporary file: {e}")
