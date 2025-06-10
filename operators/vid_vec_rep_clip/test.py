import pytest

from feluda.models.media_factory import VideoFactory
from operators.vid_vec_rep_clip import vid_vec_rep_clip


@pytest.fixture(scope="module", autouse=True)
def initialize_operator():
    vid_vec_rep_clip.initialize()


def test_sample_video_from_url():
    video_url = (
        "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
    )
    file = VideoFactory.make_from_url(video_url)
    result = vid_vec_rep_clip.run(file)
    for vec in result:
        assert len(vec.get("vid_vec")) == 512


@pytest.mark.skip(reason="This test requires a local video file.")
def test_sample_video_from_disk():
    file = VideoFactory.make_from_file_on_disk(
        "core/operators/sample_data/sample-cat-video.mp4"
    )
    result = vid_vec_rep_clip.run(file)
    for vec in result:
        assert len(vec.get("vid_vec")) == 512
