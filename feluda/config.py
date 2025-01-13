"""
This module loads configuration provided in a .yml file and makes it available as dataclasses. The main role of this module is
1. to document the possible values of various fields in the configuration file
2. assist in providing auto complete and other IDE features via type support on python.

todo :
@dennyabrain used dacite as a quick way to convert nested dicts to python dataclasess. While I am happy with its performance so far, I am happy to consider a different solution while also accounting for data validation, which is not done as of now.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional, Union

import yaml
from dacite import from_dict

log = logging.getLogger(__name__)


@dataclass
class StoreESParameters:
    host_name: str
    image_index_name: str
    text_index_name: str
    video_index_name: str
    audio_index_name: str


@dataclass
class StorePostgresParameters:
    table_names: List[str]


@dataclass
class StoreEntity:
    label: str
    type: str
    parameters: Union[StoreESParameters, StorePostgresParameters]


@dataclass
class StoreConfig:
    entities: List[StoreEntity]


@dataclass
class QueueParameters:
    host_name: str
    queues: List[dict]


@dataclass
class QueueConfig:
    label: str
    type: str
    parameters: QueueParameters


@dataclass
class ServerParameters:
    port: int
    type: str


@dataclass
class ServerConfig:
    label: str
    parameters: ServerParameters


@dataclass
class OperatorParameters:
    name: str
    type: str
    parameters: Optional[object] = None


@dataclass
class OperatorConfig:
    label: str
    parameters: List[OperatorParameters]


@dataclass
class Config:
    store: Optional[StoreConfig]
    queue: Optional[QueueConfig]
    server: Optional[ServerConfig]
    operators: Optional[OperatorConfig]


def load(filepath) -> Config:
    log.info("Loading config from " + filepath)
    with open(filepath) as f:
        parameters = yaml.safe_load(f)
    config = from_dict(data_class=Config, data=parameters)
    return config
