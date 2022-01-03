import logging

log = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

from core.feluda import Feluda
from endpoint import health, index, search

try:
    feluda = Feluda("config.yml")
    feluda.set_endpoints([health.HealthEndpoint, index.endpoint.IndexEndpoint])
    # feluda.set_endpoints([health.HealthEndpoint, index.endpoint.IndexEndpoint, search.endpoint])
    feluda.server.start()
except Exception as e:
    log.exception("Error Initializing Search Service")
