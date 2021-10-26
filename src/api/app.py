from core import config, logger
from core.server import Server
from feature.index.controller import IndexController
from feature.health import HealthController
import logging
from core.store.es_vec import ES
from queue_controller import Queue

import os

log = logging.getLogger(__name__)
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
# from feature import search
import operators
import json

# this is not needed for docker local dev but for non docker local dev. might need to document how to do this
# for non docker local development.
# load_dotenv()
try:
    parameters = config.load("config.yml")
    log.info(json.dumps(parameters, indent=4))
    # (
    #     store_param,
    #     queue_param,
    #     logger_param,
    #     server_param,
    #     operator_param,
    # ) = parameters.values()

    # logger.initialize(logger_param)
    # current_operators = operators.intialize(operator_param)

    # es_store = ES(store_param)
    # es_store.connect()
    # es_store.optionally_create_index()

    # queue = Queue(queue_param)
    # queue.connect()
    # queue.declare_queues()

    # health_controller = HealthController()
    # index_controller = IndexController(
    #     store=es_store, operators=current_operators, queue=queue
    # )

    # server = Server(
    #     server_param, controllers=[health_controller, index_controller], log=logger
    # )

    # server.start()


except Exception as e:
    log.exception("Error Initializing App")
