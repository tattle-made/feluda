import logging

log = logging.getLogger(__name__)

from typing import List
import yaml
from dataclasses import dataclass
from dacite import from_dict


@dataclass
class StoreParameters:
    host_name: str
    image_index_name: str
    text_index_name: str
    video_index_name: str


@dataclass
class StoreConfig:
    label: str
    type: str
    parameters: StoreParameters


@dataclass
class QueueParameters:
    host_name: str
    index_queue_name: str
    report_queue_name: str


@dataclass
class QueueConfig:
    label: str
    type: str
    parameters: QueueParameters


@dataclass
class LoggerParameters:
    level: str


@dataclass
class LoggerConfig:
    label: str
    parameters: LoggerParameters


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
    parameters: object


@dataclass
class OperatorConfig:
    label: str
    parameters: List[OperatorParameters]


@dataclass
class Config:
    store: StoreConfig
    queue: QueueConfig
    logger: LoggerConfig
    server: ServerConfig
    operators: OperatorConfig


def load(filepath) -> Config:
    log.info("Loading config from " + filepath)
    with open(filepath) as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)
    config = from_dict(data_class=Config, data=parameters)
    return config
