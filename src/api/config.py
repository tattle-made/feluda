import yaml
from dataclasses import dataclass
from enum import Enum


def initialize():
    global parameters, text_features, image_features, video_features, server, db, queue
    with open("config.yml") as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)
        image_features = parameters["image_features"]
        text_features = parameters["text_features"]
        video_features = parameters["video_features"]
        server = parameters["server"]
        db = parameters["db"]
        queue = parameters["queue"]
