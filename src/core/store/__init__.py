from core.config import StoreConfig
from . import es_vec
from . import postgresql

stores = {"es_vec": es_vec.ES, "postgresql": postgresql.PostgreSQLManager}

def get_stores(config: StoreConfig):
    stores_dict = {}
    for store in config.entities:
        stores_dict[store.type] = stores[store.type](store)
    return stores_dict