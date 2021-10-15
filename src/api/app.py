from feature import health
from core import config, store, logger, queue
from core.server import Server

from feature.index.controller import IndexController
from feature.health import HealthController
import logging

log = logging.getLogger(__name__)

# from feature import search
import operators

# this is not needed for docker local dev but for non docker local dev. might need to document how to do this
# for non docker local development.
# load_dotenv()
try:
    parameters = config.load("config.yml")
    (
        store_param,
        queue_param,
        logger_param,
        server_param,
        operator_param,
    ) = parameters.values()

    logger.initialize(logger_param)
    current_operators = operators.intialize(operator_param)
    index_controller = IndexController(None, operators=current_operators)
    health_controller = HealthController()

    server = Server(
        server_param, controllers=[health_controller, index_controller], log=logger
    )
    server.start()

except Exception as e:
    log.exception("Error Initializing App")
