from api.feature import health
from core import config, store, logger, queue
from core.server import Server
from feature.index import controller as IndexController
from feature.health import HealthController
from feature import search
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
        index_param,
        search_param,
    ) = parameters.values()

    logger.initialize(logger_param)
    queue.initialize(queue_param, log=logger)
    store.initialize(store_param, log=logger)

    health_controller = HealthController()
    index_controller = IndexController(index_param, store, operators.operators)
    search.initialize(search_param, index_controller, store, log=logger)

    server = Server(server_param, controllers=[index_controller, search], log=logger)
    server.start()

except Exception as e:
    print("Error Initializing app")
