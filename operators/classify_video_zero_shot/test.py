import pytest

from feluda.factory import VideoFactory

from .classify_video_zero_shot import VideoClassifier


@pytest.fixture(scope="module")
def operator():
    return VideoClassifier()


def test_sample_video_from_url(operator):
    video_url = (
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
    )
    file = VideoFactory.make_from_url(video_url)
    labels = ["cat", "dog"]
    result = operator.run(file, labels)
    assert result["prediction"] in labels
    assert isinstance(result["probs"], list)
    assert len(result["probs"]) == len(labels)


@pytest.mark.skip(reason="This test requires a local video file.")
def test_sample_video_from_disk(operator):
    file = VideoFactory.make_from_file_on_disk(
        "core/operators/sample_data/sample-cat-video.mp4"
    )
    labels = ["cat", "dog"]
    result = operator.run(file, labels)
    assert result["prediction"] in labels
    assert isinstance(result["probs"], list)
    assert len(result["probs"]) == len(labels)


def test_initialization_ffmpeg_not_found(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(RuntimeError, match="FFmpeg is not installed"):
        VideoClassifier()


def test_run_invalid_file_object(operator):
    with pytest.raises(TypeError, match="file must be a dict with a 'path' key"):
        operator.run("not_a_dict", ["cat", "dog"])


def test_run_file_not_found(operator):
    with pytest.raises(FileNotFoundError):
        operator.run({"path": "fake.mp4"}, ["cat", "dog"])


def test_run_empty_labels(operator):
    video_url = (
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
    )
    file = VideoFactory.make_from_url(video_url)
    with pytest.raises(ValueError, match="Label list must not be empty"):
        operator.run(file, [])


def test_run_labels_not_list(operator):
    video_url = (
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
    )
    file = VideoFactory.make_from_url(video_url)
    with pytest.raises(TypeError, match="labels must be a list of strings"):
        operator.run(file, "cat")


def test_run_labels_not_str(operator):
    video_url = (
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
    )
    file = VideoFactory.make_from_url(video_url)
    with pytest.raises(TypeError, match="labels must be a list of strings"):
        operator.run(file, [1, 2, 3])
