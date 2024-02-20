from core.config import StoreConfig
from . import es_vec

stores = {"es_vec": es_vec.ES}


def get_store(config: StoreConfig):
    return stores[config.type](config)
