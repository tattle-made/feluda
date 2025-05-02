import unittest
from unittest.case import skip
import os
import tracemalloc
import psutil
from feluda.models.media_factory import VideoFactory
from operators.vid_vec_rep_clip import vid_vec_rep_clip
import time
from pathlib import Path
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
            r"core/operators/sample_data/my_10min_video.mp4"
        )
        result = vid_vec_rep_clip.run(video_path)
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)

    def test_large_video_profile(self):
        
        rel_path = "5_min_video.mp4"  # just the file name
        abs_path = os.path.abspath(rel_path)
        video_path = VideoFactory.make_from_file_on_disk(abs_path)
        
        # Start CPU tracking (using psutil)
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # in MB
        cpu_times_before = process.cpu_times()
        start = time.time()

        result = vid_vec_rep_clip.run(video_path)
        end_time = time.time()
        cpu_end = process.cpu_times()

        # Stop memory tracking and get the current and peak memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()


        count = 0
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)
            count += 1

        end = time.time()
        mem_after = process.memory_info().rss / 1024 / 1024
        cpu_times_after = process.cpu_times()

        print(f"Total I-frame vectors: {count - 1}")
        print(f"Average vector included: True")
        print(f"Total vectors generated (incl. avg): {count}")
        print(f"Memory before processing: {mem_before:.2f} MB")
        print(f"Memory after processing: {mem_after:.2f} MB")
        print(f"Net memory change (test-side): {mem_after - mem_before:+.2f} MB")
        print(f"CPU time used (user + system): {(cpu_times_after.user + cpu_times_after.system) - (cpu_times_before.user + cpu_times_before.system):.2f} seconds")
        print(f"Processing time: {end - start:.2f} seconds")

    # @skip
    def test_sample_video_from_url(self):
        video_url = "https://tattle-media.s3.amazonaws.com/test-data/tattle-search/cat_vid_2mb.mp4"
        video_path = VideoFactory.make_from_url(video_url)
        result = vid_vec_rep_clip.run(video_path)
        for vec in result:
            self.assertEqual(len(vec.get("vid_vec")), 512)

