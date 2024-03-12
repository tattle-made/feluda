import unittest
from unittest.case import skip
from core.operators import vid_vec_rep_resnet
from core.models.media_factory import VideoFactory


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        vid_vec_rep_resnet.initialize(param)

    @classmethod
    def tearDownClass(cls):
        # delete config files
        pass

    @skip
    def test_sample_video_from_disk(self):
        video_path = VideoFactory.make_from_file_on_disk(
            r"core/operators/sample_data/sample-cat-video.mp4"
        )
        result = vid_vec_rep_resnet.run(video_path)
        # self.assertEqual(len(list(result)), 6)
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)

    @skip
    def test_unsupported_sample_video_from_disk(self):
        video = VideoFactory.make_from_file_on_disk(
            "core/operators/sample_data/video_files/video-1200sec.mp4"
        )
        with self.assertRaises(Exception) as context:
            vid_vec_rep_resnet.run(video)
        self.assertEqual("Video too large", str(context.exception))

    # @skip
    def test_sample_video_from_url(self):
        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        video_path = VideoFactory.make_from_url(video_url)
        result = vid_vec_rep_resnet.run(video_path)
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)
