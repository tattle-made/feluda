"""
Operator to get audio representation using LAION-CLAP - https://huggingface.co/laion/larger_clap_general
"""

def initialize(param):
    """
    Initializes the operator.
    
    Args: 
        param (dict): A dict to initialize and load the model.
    
    """
    global model, processor, librosa, contextmanager, os, torch, device

    import librosa
    from contextlib import contextmanager
    import os
    from transformers import ClapModel, ClapProcessor
    import torch

    # Load the model and processor
    model = ClapModel.from_pretrained("laion/larger_clap_general")
    processor = ClapProcessor.from_pretrained("laion/larger_clap_general")
    
    # Set the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    print("audio CLAP Model successfully initialized and loaded onto", device)


def run(audio_file):
    """
    Runs the operator and computes inference on the audio file.

    Args:
        audio_file (dict): `AudioFactory` file object.

    Returns:
        audio_emb (list): A 512-length vector embedding representing the audio. 

    """
    audio = audio_file["path"]

    @contextmanager
    def audio_load(fname):
        """
        Loads audio and removes the file after use.

        Args:
            fname (str): Path to the audio file.
        
        Yields:
            numpy.ndarray: Loaded audio data.
        """
        a, _ = librosa.load(fname, sr=48000)
        try:
            yield a
        finally:
            os.remove(fname)

    with audio_load(audio) as audio_var:
        inputs = processor(audios=audio_var, return_tensors="pt")
        inputs = {k: v.to(device) for k, v in inputs.items()} 
        with torch.no_grad():
            audio_emb = model.get_audio_features(**inputs)
        audio_emb = audio_emb.squeeze(0).tolist()
        return audio_emb
