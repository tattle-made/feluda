import types
from unittest.mock import patch

import pytest
import torch
from PIL import Image

from feluda.factory import VideoFactory

from .vid_vec_rep import VidVecRep


@pytest.fixture(scope="module")
def operator():
    operator = VidVecRep()
    return operator


def test_sample_video_from_url(operator: VidVecRep):
    video_url = (
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
    )
    file = VideoFactory.make_from_url(video_url)
    result = operator.run(file)
    for vec in result:
        assert len(vec.get("vid_vec")) == 512


@pytest.mark.skip(reason="This test requires a local video file.")
def test_sample_video_from_disk(operator: VidVecRep):
    file = VideoFactory.make_from_file_on_disk(
        "core/operators/sample_data/sample-cat-video.mp4"
    )
    result = operator.run(file)
    for vec in result:
        assert len(vec.get("vid_vec")) == 512


def test_initialization_ffmpeg_not_found(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(RuntimeError, match="FFmpeg is not installed"):
        VidVecRep()


def test_run_invalid_file_object(operator: VidVecRep):
    with pytest.raises(ValueError, match="Invalid file object"):
        operator.run("not_a_dict")


def test_run_file_not_found(operator: VidVecRep):
    with pytest.raises(FileNotFoundError):
        operator.run({"path": "fake.mp4"})


def test_extract_features_accepts_plain_tensor(operator: VidVecRep):
    # transformers <5.0 behavior: get_image_features() returns the tensor directly.
    plain_tensor = torch.randn(1, 512)
    image = Image.new("RGB", (32, 32))
    with patch.object(operator.model, "get_image_features", return_value=plain_tensor):
        features = operator.extract_features([image])
    assert features is plain_tensor


def test_extract_features_unwraps_transformers_v5_output(operator: VidVecRep):
    # transformers >=5.0 wraps get_image_features()'s return in a BaseModelOutputWithPooling
    # instead of returning a plain tensor (huggingface/transformers PR #42564). Simulated
    # via a stand-in object rather than depending on which transformers version is actually
    # installed in CI.
    wrapped_output = types.SimpleNamespace(pooler_output=torch.randn(1, 512))
    image = Image.new("RGB", (32, 32))
    with patch.object(operator.model, "get_image_features", return_value=wrapped_output):
        features = operator.extract_features([image])
    assert isinstance(features, torch.Tensor)
    assert features is wrapped_output.pooler_output
