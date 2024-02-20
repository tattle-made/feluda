import logging

log = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

from core.feluda import ComponentType, Feluda
from endpoint import health, index, search

try:
    feluda = Feluda("config-server.yml")
    feluda.set_endpoints(
        [health.HealthEndpoint, index.endpoint.IndexEndpoint, search.SearchEndpoint]
    )
    # feluda.set_endpoints([health.HealthEndpoint, index.endpoint.IndexEndpoint, search.endpoint])
    # feluda.server.start()
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    feluda.start_component(ComponentType.SERVER)
except Exception as e:
    log.exception("Error Initializing Search Service")
