import yaml
from dataclasses import dataclass


def load(filepath):
    with open(filepath) as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)
    return parameters
