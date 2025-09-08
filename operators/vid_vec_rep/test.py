import pytest

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
