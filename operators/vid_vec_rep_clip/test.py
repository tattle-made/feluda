import unittest
from unittest.case import skip
from unittest import TestCase, skip
import os
from feluda.models.media_factory import VideoFactory
from operators.vid_vec_rep_clip import vid_vec_rep_clip
from benchmark.vid_vec_rep_clip.profiler import profile_large_video

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize operator
        param = {}
        vid_vec_rep_clip.initialize(param)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_sample_video_from_url(self):
        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        video_path = VideoFactory.make_from_url(video_url)
        profile_large_video(video_path["path"])

    @skip
    def test_sample_video_from_disk(self):
        video_path = VideoFactory.make_from_file_on_disk(
            r"core/operators/sample_data/my_10min_video.mp4"
        )

        profile_large_video(video_path)


    def test_large_video_profile(self):
        
        rel_path = "1_min_video.mp4"  # optional: keep if you use it elsewhere
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_path))

        profile_large_video(abs_path)