import tempfile
import unittest

import numpy as np
import yaml

from feluda import Feluda
from feluda.models.media_factory import VideoFactory


class TestFeludaClassifyVideoZeroShotIntegration(unittest.TestCase):
    """
    Integration test for Feluda and classify-video-zero-shot operator.
    This test validates the integration between:
    - feluda (core)
    - feluda-classify-video-zero-shot
    """

    @classmethod
    def setUpClass(cls):
        """Create a temporary test configuration file that will be used for all tests."""

        # Setup configuration with the video zero-shot classifier operator
        cls.config = {
            "operators": {
                "label": "Operators",
                "parameters": [
                    {
                        "name": "video classifier",
                        "type": "classify_video_zero_shot",
                        "parameters": {}
                    }
                ],
            }
        }

        fd, cls.config_path = tempfile.mkstemp(suffix=".yml")
        with open(fd, "w") as f:
            yaml.dump(cls.config, f)

        cls.feluda = Feluda(cls.config_path)
        cls.feluda.setup()

        cls.test_video_url = "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"

        cls.sample_labels = ["cat", "dog", "car", "building", "people"]

    def setUp(self):
        """Setup before each test method."""
        self.operator = self.feluda.operators.get()["classify_video_zero_shot"]

    def test_operator_availability(self):
        """Test that the classify_video_zero_shot operator is available."""
        self.assertIsNotNone(self.operator, "Operator should be available in the system")
        self.assertTrue(hasattr(self.operator, "run"), "Operator should have a 'run' method")

    def test_video_object_generation(self):
        """Test that video object generation works end-to-end."""
        video_obj = VideoFactory.make_from_url(self.test_video_url)

        self.assertIsNotNone(video_obj, "Video object should not be None")
        self.assertIn("path", video_obj, "Video object should have a path attribute")
        self.assertTrue(video_obj["path"], "Video path should not be empty")

    def test_video_classification_structure(self):
        """Test video classification structure using zero-shot classifier."""

        video_obj = VideoFactory.make_from_url(self.test_video_url)
        result = self.operator.run(video_obj, self.sample_labels)

        # Verify result structure
        self.assertIsNotNone(result, "Classification result should not be None")
        self.assertTrue(isinstance(result, dict), "Result should be a dictionary")

        # Check that result contains the expected keys
        self.assertIn("prediction", result, "Result should contain a 'prediction' key")
        self.assertIn("probs", result, "Result should contain a 'probs' key")

        # Check prediction is a string and one of our labels
        self.assertTrue(isinstance(result["prediction"], str), "Prediction should be a string")
        self.assertIn(result["prediction"], self.sample_labels, "Prediction should be one of the provided labels")

        # Check probs is a list with the correct length
        self.assertTrue(isinstance(result["probs"], list), "Probs should be a list")
        self.assertEqual(len(result["probs"]), len(self.sample_labels), "Length of probs should match number of labels")

        # Check probabilities sum close to 1 (allowing for small floating point errors)
        self.assertAlmostEqual(sum(result["probs"]), 1.0, places=len(self.sample_labels), msg="Probabilities should sum to approximately 1")
        # Check each probability is a float between 0 and 1
        for prob in result["probs"]:
            self.assertTrue(isinstance(prob, float), "Each probability should be a float")
            self.assertTrue(0 <= prob <= 1, "Each probability should be between 0 and 1")

    def test_video_classification_results(self):
        """Test video classification results using zero-shot classifier."""

        # Create video object
        video_obj = VideoFactory.make_from_url(self.test_video_url)

        # Perform classification
        result = self.operator.run(video_obj, self.sample_labels)

        # For a cat video, "cat" should be the highest probability label
        self.assertEqual(result["prediction"], "cat", "Prediction should be 'cat' for a cat video")

        # The first probability (for "cat") should be highest
        max_prob_index = np.argmax(result["probs"])
        self.assertEqual(max_prob_index, 0, "Highest probability should be for 'cat' (first label)")

        # The "cat" probability should be significantly higher than others
        cat_prob = result["probs"][0]
        other_probs = result["probs"][1:]
        self.assertTrue(all(cat_prob > p for p in other_probs), "Cat probability should be higher than all other probabilities")

        # The cat probability should be reasonably high (based on the sample output)
        self.assertGreater(cat_prob, 0.5, "Cat probability should be at least 0.5")

    def test_result_consistency(self):
        """Test that results are consistent across multiple runs."""

        # Create video object (reusing the same video)
        video_obj = VideoFactory.make_from_url(self.test_video_url)

        # Run classification twice
        result1 = self.operator.run(video_obj, self.sample_labels)

        # Need to create a new video object since the previous one's file was deleted
        video_obj2 = VideoFactory.make_from_url(self.test_video_url)
        result2 = self.operator.run(video_obj2, self.sample_labels)

        # Check that predictions are the same
        self.assertEqual(result1["prediction"], result2["prediction"],
                        "Predictions should be consistent across runs")

        # Check that probabilities are similar (may not be identical due to frame extraction)
        for i, (p1, p2) in enumerate(zip(result1["probs"], result2["probs"])):
            # Allow for some variation but should be close
            self.assertAlmostEqual(p1, p2, places=1,
                                msg=f"Probabilities for label {self.sample_labels[i]} should be similar")

    def test_different_labels(self):
        """Test classification with different labels."""

        # Create video object
        video_obj = VideoFactory.make_from_url(self.test_video_url)

        # Different set of labels
        different_labels = ["feline", "animal", "vehicle", "nature", "technology"]

        # Perform classification
        result = self.operator.run(video_obj, different_labels)

        # Check basic structure
        self.assertIn("prediction", result)
        self.assertIn("probs", result)
        self.assertEqual(len(result["probs"]), len(different_labels))

        # For a cat video, "feline" or "animal" should be the top predictions
        predicted_label = result["prediction"]
        self.assertIn(predicted_label, ["feline", "animal"],
                     f"Prediction should be 'feline' or 'animal' for a cat video, got '{predicted_label}'")

        # Probabilities for feline/animal should be higher than others
        feline_index = different_labels.index("feline")
        animal_index = different_labels.index("animal")

        feline_prob = result["probs"][feline_index]
        animal_prob = result["probs"][animal_index]

        # Other probabilities
        other_indices = [i for i in range(len(different_labels)) if i != feline_index and i != animal_index]
        other_probs = [result["probs"][i] for i in other_indices]

        # Either feline or animal should have significantly higher probability
        self.assertTrue(feline_prob > max(other_probs) or animal_prob > max(other_probs),
                       "Either 'feline' or 'animal' should have higher probability than other labels")

    def test_empty_labels_list(self):
        """Test handling of empty labels list."""
        # Create video object
        video_obj = VideoFactory.make_from_url(self.test_video_url)

        # Test with empty labels list - should raise ValueError
        with self.assertRaises(ValueError):
            self.operator.run(video_obj, [])

    def test_invalid_video_input(self):
        """Test handling of invalid video input."""
        # Test with None input
        with self.assertRaises(Exception):
            self.operator.run(None, self.sample_labels)

        # Test with invalid video object (missing path)
        invalid_video = {"type": "video", "url": "invalid"}
        with self.assertRaises(Exception):
            self.operator.run(invalid_video, self.sample_labels)
