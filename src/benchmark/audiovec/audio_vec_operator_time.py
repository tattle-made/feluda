import time
from core.operators import audio_vec_embedding


def find_time():
    file_path = {"path": r"core/operators/sample_data/audio.wav"}
    audio_vec_embedding.initialize(param=None)
    start_time = time.time()
    audio_vec_embedding.run(file_path)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken - {duration}")


if __name__ == "__main__":
    find_time()
