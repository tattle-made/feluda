import unittest
from unittest.case import skip

from feluda.models.media_factory import VideoFactory
from operators.vid_vec_rep_clip import vid_vec_rep_clip


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        vid_vec_rep_clip.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    @skip
    def test_sample_video_from_disk(self):
        video_path = VideoFactory.make_from_file_on_disk(
            r"core/operators/sample_data/sample-cat-video.mp4"
        )
        result = vid_vec_rep_clip.run(video_path)
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)

    # @skip
    def test_sample_video_from_url(self):
        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        video_path = VideoFactory.make_from_url(video_url)
        result = vid_vec_rep_clip.run(video_path)
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)
