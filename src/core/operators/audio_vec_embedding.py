def initialize(param):
    global model
    global librosa
    global np
    global contextmanager
    global os

    import numpy as np
    import librosa

    # from panns_inference import AudioTagging
    from core.operators.audio_cnn_model.inference import AudioTagging
    from contextlib import contextmanager
    import os

    # load the default model into cpu.
    model = AudioTagging(checkpoint_path=None, device="cpu")
    print("model successfully downloaded")


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def run(audio_file):
    audio = audio_file["path"]

    @contextmanager
    def audio_load(fname):
        a, _ = librosa.load(fname, sr=44100)
        try:
            yield a
        finally:
            os.remove(fname)

    with audio_load(audio) as audio_var:
        query_audio = audio_var[None, :]
        _, emb = model.inference(query_audio)
        normalized_v = normalize(emb[0])
        return normalized_v


# if __name__ == "__main__":
#     initialize(param={})
#     audio_file_path = {"path": r"core/operators/sample_data/audio.wav"}
#     audio_emb = run(audio_file_path)
#     audio_emb_list = audio_emb.tolist()
#     print(len(audio_emb_list))
