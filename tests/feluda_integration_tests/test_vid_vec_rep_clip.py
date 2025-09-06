import os
from pathlib import Path

import numpy as np
import pytest
from vid_vec_rep import VidVecRep

from feluda.factory import VideoFactory


@pytest.fixture(scope="session")
def video_operator():
    """Fixture to provide video vector representation operator."""
    return VidVecRep()


@pytest.fixture(scope="session")
def test_video_url():
    """Fixture to provide test video URL."""
    return "https://github.com/tattle-made/feluda_datasets/raw/main/feluda-sample-media/sample-cat-video.mp4"


@pytest.fixture(scope="session")
def expected_vector_dim():
    """Fixture to provide expected vector dimension."""
    return 512


class TestVideoVectorGeneration:
    """Test video vector generation functionality."""

    def test_video_vector_generation(
        self, video_operator, test_video_url, expected_vector_dim
    ):
        """Test that video vector generation works end-to-end."""
        video_object = VideoFactory.make_from_url(test_video_url)
        downloaded_path = video_object.get("path")
        assert downloaded_path is not None, "VideoFactory did not return a path"
        assert Path(downloaded_path).exists(), (
            f"Downloaded file not found at {downloaded_path}"
        )

        vector_generator = video_operator.run(video_object)

        try:
            first_output_item = next(vector_generator)
        except Exception as e:
            if Path(downloaded_path).exists():
                os.remove(downloaded_path)
            raise AssertionError(
                f"Calling next on generator raised an unexpected error: {e}"
            )

        assert isinstance(first_output_item, dict), (
            "Operator did not yield a dictionary"
        )
        assert "vid_vec" in first_output_item, (
            "Yielded dictionary missing 'vid_vec' key"
        )
        assert "is_avg" in first_output_item, "Yielded dictionary missing 'is_avg' key"

        actual_vector = first_output_item["vid_vec"]
        is_average = first_output_item["is_avg"]

        assert is_average, "First yielded vector should have is_avg=True"

        assert isinstance(actual_vector, list), "Vector ('vid_vec') should be a list"
        assert len(actual_vector) > 0, "Vector should not be empty"
        assert len(actual_vector) == expected_vector_dim, (
            f"Vector should have dimension {expected_vector_dim}"
        )

        vector_np = np.array(actual_vector)
        assert not np.all(vector_np == 0), "Vector should not be all zeros"
        assert not np.any(np.isnan(vector_np)), "Vector should not contain NaN values"

    def test_video_vector_consistency(self, video_operator, test_video_url):
        """Test that generating vectors twice from the same video gives consistent results."""
        video_obj = VideoFactory.make_from_url(test_video_url)
        vec1_generator = video_operator.run(video_obj)
        vec1 = next(vec1_generator)["vid_vec"]

        video_obj = VideoFactory.make_from_url(test_video_url)
        vec2_generator = video_operator.run(video_obj)
        vec2 = next(vec2_generator)["vid_vec"]

        np.testing.assert_almost_equal(
            vec1,
            vec2,
            decimal=5,
            err_msg="Vectors should be nearly identical for the same video",
        )


@pytest.fixture(scope="session", autouse=True)
def cleanup_operators(video_operator):
    """Cleanup operators after each test."""
    yield
    video_operator.cleanup()
