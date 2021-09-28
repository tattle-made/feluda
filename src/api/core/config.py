import yaml
from dataclasses import dataclass
from enum import Enum


def load(filepath):
    with open(filepath) as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)
    return parameters
