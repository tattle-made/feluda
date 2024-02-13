def initialize(param):
    global model
    global librosa
    global np

    import numpy as np
    import librosa
    from panns_inference import AudioTagging

    # load the default model into cpu.
    model = AudioTagging(checkpoint_path=None, device='cpu')
    print('model successfully downloaded')

# Function to normalize a vector. Normalizing a vector means adjusting the values measured in different scales to a common scale.
def normalize(v):
   # np.linalg.norm computes the vector's norm (magnitude). The norm is the total length of all vectors in a space.
   norm = np.linalg.norm(v)
   if norm == 0:
        return v
   # Return the normalized vector.
   return v / norm

def run(audio_file):
    # Load the audio file using librosa's load function, which returns an audio time series and its corresponding sample rate.
    a, _ = librosa.load(audio_file, sr=44100)
    # Reshape the audio time series to have an extra dimension, which is required by the model's inference function.
    query_audio = a[None, :]
    # Perform inference on the reshaped audio using the model. This returns an embedding of the audio.
    _, emb = model.inference(query_audio)
    # Normalize the embedding. This scales the embedding to have a length (magnitude) of 1, while maintaining its direction.
    normalized_v = normalize(emb[0])
    # Return the normalized embedding required for dot_product elastic similarity dense vector
    return normalized_v

# if __name__ == "__main__":
#     import time
#     audio_file_path = r'sample_data/audio.wav'
#     initialize(param={})
#     audio_emb = run(audio_file_path)
#     audio_emb_list = audio_emb.tolist()
#     print(audio_emb_list)