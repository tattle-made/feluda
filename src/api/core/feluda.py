import logging

log = logging.getLogger(__name__)

from core import config
from core.server import Server
from core import queue
from core.operators import Operator
from core import store


class Feluda:
    def __init__(self, configPath):
        self.config = config.load(configPath)
        self.operators = Operator(self.config.operators)
        self.store = store.get_store(self.config.store)
        self.queue = queue.Queue(self.config.queue)
        self.server = Server(self.config.server)

    def start(self):
        try:
            self.store.connect()
            self.store.create_index()
        except Exception:
            log.exception("Could not connect to Store")
            raise Exception("Could not connect to Store")

        try:
            self.queue.connect()
            self.queue.declare_queues()
        except Exception:
            log.exception("Could not connect to Queue")
            raise Exception("Could not connect to Queue")

        self.server.start()

    def set_endpoints(self, endpoints):
        for endpoint in endpoints:
            self.server.add_endpoint(endpoint(self))

        self.server.enable_endpoints()

    def get_state(self):
        pass
