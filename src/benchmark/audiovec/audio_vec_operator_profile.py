from core.operators import audio_vec_embedding


def profile_code():
    file_path = {"path": r"core/operators/sample_data/audio.wav"}
    audio_vec_embedding.initialize(param=None)
    audio_vec_embedding.run(file_path)
    print("audio vec profiler complete!")


if __name__ == "__main__":
    profile_code()
