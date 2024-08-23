"""Operator to get audio representation using LAION-CLAP - https://github.com/LAION-AI/CLAP. """

def initialize(param):
    """
    Initializes the operator.
    
    Args: 
        param (dict): A dict to initialize and load the the model.
    
    """
    global model
    global librosa
    global np
    global contextmanager
    global os

    import numpy as np
    import librosa
    from contextlib import contextmanager
    import os
    import laion_clap
    
    model = laion_clap.CLAP_Module()
    model.load_ckpt() # load the best checkpoint (HTSAT model) in the paper.
    print("model successfully downloaded")


def run(audio_file):
    """
    Runs the operator and compute inference on the audio file.

    Args:
        audio_file (dict): `AudioFactory` file object.

    Returns:
        audio_emb (numpy.ndarray): A 512-length vector embedding representing the audio. 

    """
    audio = audio_file["path"]

    @contextmanager
    def audio_load(fname):
        a, _ = librosa.load(fname, sr=48000)
        try:
            yield a
        finally:
            os.remove(fname)

    with audio_load(audio) as audio_var:
        query_audio = audio_var.reshape(1, -1)
        audio_emb = model.get_audio_embedding_from_data(x = query_audio, use_tensor=False)
        audio_emb = audio_emb.reshape(-1)
        return audio_emb
