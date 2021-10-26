import logging

log = logging.getLogger(__name__)
import yaml


def load(filepath):
    log.info("Loading config.")
    with open(filepath) as f:
        parameters = yaml.load(f, Loader=yaml.FullLoader)
    return parameters
