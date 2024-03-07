def initialize(param):
    global model
    global librosa
    global np

    import numpy as np
    import librosa
    # from panns_inference import AudioTagging
    from core.operators.audio_cnn_model.inference import AudioTagging
    # import os

    # load the default model into cpu.
    model = AudioTagging(checkpoint_path=None, device='cpu')
    print('model successfully downloaded')

def normalize(v):
   norm = np.linalg.norm(v)
   if norm == 0:
        return v
   return v / norm

def run(audio_file):
    audio = audio_file["path"]
    a, _ = librosa.load(audio, sr=44100)
    query_audio = a[None, :]
    _, emb = model.inference(query_audio)
    normalized_v = normalize(emb[0])
    return normalized_v

# if __name__ == "__main__":
#     initialize(param={})
#     audio_file_path = {"path": r'sample_data/audio.wav'}
#     audio_emb = run(audio_file_path)
#     audio_emb_list = audio_emb.tolist()
#     print(len(audio_emb_list))