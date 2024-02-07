import cProfile
import pstats
from io import StringIO
from core.operators import vid_vec_rep_resnet

def profile_code():
    file_path = {"path": r"core/operators/sample_data/sample-cat-video.mp4"}
    vid_vec_rep_resnet.initialize(param=None)
    profiler = cProfile.Profile()
    profiler.enable()
    vid_vec_rep_resnet.run(file_path)
    profiler.disable()
    result_stream = StringIO()
    stats = pstats.Stats(profiler, stream=result_stream).sort_stats('cumulative')
    stats.print_stats()
    print(result_stream.getvalue())

if __name__ == "__main__":
    profile_code()