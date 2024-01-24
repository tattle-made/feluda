import unittest
import vid_vec_rep_resnet
# from feature.index.model import VideoFactory
from unittest.case import skip


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

    def test_sample_video_from_disk(self):
        video = {"path": r"sample_data/sample-cat-video.mp4"}
        result = vid_vec_rep_resnet.run(video)
        self.assertEqual(len(list(result)), 6)

    @skip
    def test_unsupported_sample_video_from_disk(self):
        video = VideoFactory.make_from_file_on_disk("sample_data/cat_vid_94mb.mp4")
        with self.assertRaises(Exception) as context:
            vid_vec_rep_resnet.run(video)
        self.assertTrue("Video too large" in str(context.exception))

    @skip
    def test_sample_video_from_url(self):
        import wget

        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        video_path = "/tmp/video_file.mp4"
        wget.download(video_url, out=video_path)
        video = VideoFactory.make_from_file_on_disk(video_path)

        avg_vec, all_vec = vid_vec_rep_resnet.run(video)
        self.assertEqual(len(avg_vec), 512)
        for vec in all_vec:
            self.assertEqual(len(vec), 512)
