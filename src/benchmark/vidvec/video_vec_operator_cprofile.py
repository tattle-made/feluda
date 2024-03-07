import cProfile
import pstats
from io import StringIO
from core.operators import vid_vec_rep_resnet
from core.models.media_factory import VideoFactory


def profile_code():
    vid_vec_rep_resnet.initialize(param=None)
    video_url = "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4"
    video_path = VideoFactory.make_from_url(video_url)
    profiler = cProfile.Profile()
    profiler.enable()
    vid_vec_rep_resnet.run(video_path)
    profiler.disable()
    result_stream = StringIO()
    stats = pstats.Stats(profiler, stream=result_stream).sort_stats("cumulative")
    stats.print_stats()
    print(result_stream.getvalue())
    print("Video vec c-profiler complete!")


if __name__ == "__main__":
    profile_code()
