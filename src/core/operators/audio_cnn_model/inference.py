import os

# import numpy as np
# import argparse
# import librosa
# import matplotlib.pyplot as plt
import torch
from pathlib import Path
import wget

from .pytorch_utils import move_data_to_device
from .models import Cnn14  # , Cnn14_DecisionLevelMax
from .config import labels, classes_num


def create_folder(fd):
    if not os.path.exists(fd):
        os.makedirs(fd)


def get_filename(path):
    path = os.path.realpath(path)
    na_ext = path.split("/")[-1]
    na = os.path.splitext(na_ext)[0]
    return na


class AudioTagging(object):
    def __init__(self, model=None, checkpoint_path=None, device="cuda"):
        """Audio tagging inference wrapper."""
        if not checkpoint_path:
            checkpoint_path = "{}/panns_data/Cnn14_mAP=0.431.pth".format(
                str(Path.home())
            )
        print("Checkpoint path: {}".format(checkpoint_path))

        if (
            not os.path.exists(checkpoint_path)
            or os.path.getsize(checkpoint_path) < 3e8
        ):
            create_folder(os.path.dirname(checkpoint_path))
            zenodo_path = "https://github.com/tattle-made/feluda/releases/download/third-party-models/Cnn14_mAP.0.431.pth"
            # os.system('wget -O "{}" "{}"'.format(checkpoint_path, zenodo_path))
            wget.download(zenodo_path, out=checkpoint_path)

        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # checkpoint_path = os.path.join(script_dir, 'panns_data', 'Cnn14_mAP=0.431.pth')
        print(checkpoint_path)

        if device == "cuda" and torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"

        self.labels = labels
        self.classes_num = classes_num

        # Model
        if model is None:
            self.model = Cnn14(
                sample_rate=32000,
                window_size=1024,
                hop_size=320,
                mel_bins=64,
                fmin=50,
                fmax=14000,
                classes_num=self.classes_num,
            )
        else:
            self.model = model

        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model"])

        # Parallel
        if "cuda" in str(self.device):
            self.model.to(self.device)
            print("GPU number: {}".format(torch.cuda.device_count()))
            self.model = torch.nn.DataParallel(self.model)
        else:
            print("Using CPU.")

    def inference(self, audio):
        audio = move_data_to_device(audio, self.device)

        with torch.no_grad():
            self.model.eval()
            output_dict = self.model(audio, None)

        clipwise_output = output_dict["clipwise_output"].data.cpu().numpy()
        embedding = output_dict["embedding"].data.cpu().numpy()

        return clipwise_output, embedding
