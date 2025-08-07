import numpy as np
import pytest
from classify_video_zero_shot import VideoClassifier

from feluda.factory import VideoFactory


@pytest.fixture(scope="session")
def video_classifier_operator():
    """Fixture to provide video zero-shot classifier operator."""
    return VideoClassifier()


@pytest.fixture(scope="session")
def test_video_url():
    """Fixture to provide test video URL."""
    return "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"


@pytest.fixture(scope="session")
def sample_labels():
    """Fixture to provide sample labels for classification."""
    return ["cat", "dog", "car", "building", "people"]


class TestVideoZeroShotClassification:
    """Test video zero-shot classification functionality."""

    def test_operator_availability(self, video_classifier_operator):
        """Test that the classify_video_zero_shot operator is available."""
        assert video_classifier_operator is not None, (
            "Operator should be available in the system"
        )
        assert hasattr(video_classifier_operator, "run"), (
            "Operator should have a 'run' method"
        )

    def test_video_object_generation(self, test_video_url):
        """Test that video object generation works end-to-end."""
        video_obj = VideoFactory.make_from_url(test_video_url)

        assert video_obj is not None, "Video object should not be None"
        assert "path" in video_obj, "Video object should have a path attribute"
        assert video_obj["path"], "Video path should not be empty"

    def test_video_classification_structure(
        self, video_classifier_operator, test_video_url, sample_labels
    ):
        """Test video classification structure using zero-shot classifier."""
        video_obj = VideoFactory.make_from_url(test_video_url)
        result = video_classifier_operator.run(video_obj, sample_labels)

        # Verify result structure
        assert result is not None, "Classification result should not be None"
        assert isinstance(result, dict), "Result should be a dictionary"

        # Check that result contains the expected keys
        assert "prediction" in result, "Result should contain a 'prediction' key"
        assert "probs" in result, "Result should contain a 'probs' key"

        # Check prediction is a string and one of our labels
        assert isinstance(result["prediction"], str), "Prediction should be a string"
        assert result["prediction"] in sample_labels, (
            "Prediction should be one of the provided labels"
        )

        # Check probs is a list with the correct length
        assert isinstance(result["probs"], list), "Probs should be a list"
        assert len(result["probs"]) == len(sample_labels), (
            "Length of probs should match number of labels"
        )

        # Check probabilities sum close to 1 (allowing for small floating point errors)
        assert abs(sum(result["probs"]) - 1.0) < 1e-6, (
            "Probabilities should sum to approximately 1"
        )

        # Check each probability is a float between 0 and 1
        for prob in result["probs"]:
            assert isinstance(prob, float), "Each probability should be a float"
            assert 0 <= prob <= 1, "Each probability should be between 0 and 1"

    def test_video_classification_results(
        self, video_classifier_operator, test_video_url, sample_labels
    ):
        """Test video classification results using zero-shot classifier."""
        # Create video object
        video_obj = VideoFactory.make_from_url(test_video_url)

        # Perform classification
        result = video_classifier_operator.run(video_obj, sample_labels)

        # For a cat video, "cat" should be the highest probability label
        assert result["prediction"] == "cat", (
            "Prediction should be 'cat' for a cat video"
        )

        # The first probability (for "cat") should be highest
        max_prob_index = np.argmax(result["probs"])
        assert max_prob_index == 0, (
            "Highest probability should be for 'cat' (first label)"
        )

        # The "cat" probability should be significantly higher than others
        cat_prob = result["probs"][0]
        other_probs = result["probs"][1:]
        assert all(cat_prob > p for p in other_probs), (
            "Cat probability should be higher than all other probabilities"
        )

        # The cat probability should be reasonably high (based on the sample output)
        assert cat_prob > 0.5, "Cat probability should be at least 0.5"

    def test_result_consistency(
        self, video_classifier_operator, test_video_url, sample_labels
    ):
        """Test that results are consistent across multiple runs."""
        # Create video object (reusing the same video)
        video_obj = VideoFactory.make_from_url(test_video_url)

        # Run classification twice
        result1 = video_classifier_operator.run(video_obj, sample_labels)

        # Need to create a new video object since the previous one's file was deleted
        video_obj2 = VideoFactory.make_from_url(test_video_url)
        result2 = video_classifier_operator.run(video_obj2, sample_labels)

        # Check that predictions are the same
        assert result1["prediction"] == result2["prediction"], (
            "Predictions should be consistent across runs"
        )

        # Check that probabilities are similar (may not be identical due to frame extraction)
        for i, (p1, p2) in enumerate(
            zip(result1["probs"], result2["probs"], strict=False)
        ):
            # Allow for some variation but should be close
            assert abs(p1 - p2) < 0.1, (
                f"Probabilities for label {sample_labels[i]} should be similar"
            )

    def test_different_labels(self, video_classifier_operator, test_video_url):
        """Test classification with different labels."""
        # Create video object
        video_obj = VideoFactory.make_from_url(test_video_url)

        # Different set of labels
        different_labels = ["feline", "animal", "vehicle", "nature", "technology"]

        # Perform classification
        result = video_classifier_operator.run(video_obj, different_labels)

        # Check basic structure
        assert "prediction" in result
        assert "probs" in result
        assert len(result["probs"]) == len(different_labels)

        # For a cat video, "feline" or "animal" should be the top predictions
        predicted_label = result["prediction"]
        assert predicted_label in ["feline", "animal"], (
            f"Prediction should be 'feline' or 'animal' for a cat video, got '{predicted_label}'"
        )

        # Probabilities for feline/animal should be higher than others
        feline_index = different_labels.index("feline")
        animal_index = different_labels.index("animal")

        feline_prob = result["probs"][feline_index]
        animal_prob = result["probs"][animal_index]

        # Other probabilities
        other_indices = [
            i
            for i in range(len(different_labels))
            if i != feline_index and i != animal_index
        ]
        other_probs = [result["probs"][i] for i in other_indices]

        # Either feline or animal should have significantly higher probability
        assert feline_prob > max(other_probs) or animal_prob > max(other_probs), (
            "Either 'feline' or 'animal' should have higher probability than other labels"
        )

    def test_empty_labels_list(self, video_classifier_operator, test_video_url):
        """Test handling of empty labels list."""
        # Create video object
        video_obj = VideoFactory.make_from_url(test_video_url)

        # Test with empty labels list - should raise ValueError
        with pytest.raises(ValueError):
            video_classifier_operator.run(video_obj, [])

    def test_invalid_video_input(self, video_classifier_operator, sample_labels):
        """Test handling of invalid video input."""
        # Test with None input
        with pytest.raises(Exception):
            video_classifier_operator.run(None, sample_labels)

        # Test with invalid video object (missing path)
        invalid_video = {"type": "video", "url": "invalid"}
        with pytest.raises(Exception):
            video_classifier_operator.run(invalid_video, sample_labels)


@pytest.fixture(scope="session", autouse=True)
def cleanup_operators(video_classifier_operator):
    """Cleanup operators after each test."""
    yield
    video_classifier_operator.cleanup()
