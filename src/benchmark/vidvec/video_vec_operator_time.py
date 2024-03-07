import time
from core.operators import vid_vec_rep_resnet
from core.models.media_factory import VideoFactory


def find_time():
    vid_vec_rep_resnet.initialize(param=None)
    video_url = "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4"
    video_path = VideoFactory.make_from_url(video_url)
    start_time = time.time()
    vid_vec_rep_resnet.run(video_path)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken - {duration}")
    print("Video vec time profile complete!")


if __name__ == "__main__":
    find_time()
