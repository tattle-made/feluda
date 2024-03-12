import cProfile
import pstats
from io import StringIO
from core.operators import audio_vec_embedding


def profile_code():
    file_path = {"path": r"core/operators/sample_data/audio.wav"}
    audio_vec_embedding.initialize(param=None)
    profiler = cProfile.Profile()
    profiler.enable()
    audio_vec_embedding.run(file_path)
    profiler.disable()
    result_stream = StringIO()
    stats = pstats.Stats(profiler, stream=result_stream).sort_stats("cumulative")
    stats.print_stats()
    print(result_stream.getvalue())


if __name__ == "__main__":
    profile_code()
