# The config module loads configuration provided in a .yml file and makes it available as dataclasses. The main role of this module is
# 1. to document the possible values of various fields in the configuration file
# 2. assist in providing auto complete and other IDE features via type support on python.

# TODO : @dennyabrain used dacite as a quick way to convert nested dicts to python dataclasess. While I am happy with its performance so far, I am happy to consider a different solution while also accounting for data validation, which is not done as of now.

import logging
from dataclasses import dataclass

import yaml
from dacite import from_dict

log = logging.getLogger(__name__)


@dataclass
class StoreESParameters:
    """Parameters for Elasticsearch store configuration."""

    host_name: str
    image_index_name: str
    text_index_name: str
    video_index_name: str
    audio_index_name: str


@dataclass
class StorePostgresParameters:
    """Parameters for PostgreSQL store configuration."""

    table_names: list[str]


@dataclass
class StoreEntity:
    """Entity configuration for the store."""

    label: str
    type: str
    parameters: StoreESParameters | StorePostgresParameters


@dataclass
class StoreConfig:
    """Configuration for the store."""

    entities: list[StoreEntity]


@dataclass
class QueueParameters:
    """Parameters for queue configuration."""

    host_name: str
    queues: list[dict]


@dataclass
class QueueConfig:
    """Configuration for the queue."""

    label: str
    type: str
    parameters: QueueParameters


@dataclass
class ServerParameters:
    """Parameters for server configuration."""

    port: int
    type: str


@dataclass
class ServerConfig:
    """Configuration for the server."""

    label: str
    parameters: ServerParameters


@dataclass
class OperatorParameters:
    """Parameters for operator configuration."""

    name: str
    type: str
    parameters: object | None = None


@dataclass
class OperatorConfig:
    """Configuration for operators."""

    label: str
    parameters: list[OperatorParameters]


@dataclass
class Config:
    """Main configuration class for the Feluda framework."""

    store: StoreConfig | None
    queue: QueueConfig | None
    server: ServerConfig | None
    operators: OperatorConfig | None


def load(filepath: str) -> Config:
    """Load configuration from a YAML file and return a Config dataclass."""
    log.info("Loading config from " + filepath)
    with open(filepath) as f:
        parameters = yaml.safe_load(f)
    config = from_dict(data_class=Config, data=parameters)
    return config
