import os
import time
import tracemalloc

import psutil

from feluda.models.media_factory import VideoFactory
from operators.vid_vec_rep_clip import vid_vec_rep_clip


def profile_large_video(abs_path):
    video_path = VideoFactory.make_from_file_on_disk(abs_path)

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024
    cpu_times_before = process.cpu_times()
    start = time.time()

    tracemalloc.start()
    result = vid_vec_rep_clip.run(video_path)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    cpu_times_after = process.cpu_times()
    mem_after = process.memory_info().rss / 1024 / 1024

    count = 0
    for vec in result:
        assert len(vec.get("vid_vec")) == 512
        count += 1

    print(f"Total I-frame vectors: {count - 1}")
    print("Average vector included: True")
    print(f"Total vectors generated (incl. avg): {count}")
    print(f"Memory before processing: {mem_before:.2f} MB")
    print(f"Memory after processing: {mem_after:.2f} MB")
    print(f"Net memory change (test-side): {mem_after - mem_before:+.2f} MB")
    print(
        f"CPU time used (user + system): {(cpu_times_after.user + cpu_times_after.system) - (cpu_times_before.user + cpu_times_before.system):.2f} seconds"
    )
    print(f"Processing time: {end_time - start:.2f} seconds")
