import logging

log = logging.getLogger(__name__)

from core import config, store
from core.server import Server
from core.operators import Operator
from core.queue import Queue


class Feluda:
    def __init__(self, configPath):
        self.config = config.load(configPath)
        self.operators = Operator(self.config.operators)
        self.store = store.get_store(self.config.store)
        self.queue = Queue(self.config.queue)
        self.server = Server(self.config.server)

    def set_endpoints(self, endpoints):
        for endpoint in endpoints:
            self.server.add_endpoint(endpoint(self))

        self.server.enable_endpoints()

    def start(self):
        self.store.connect()
        self.store.create_index()

        self.queue.connect()
        self.queue.declare_queues()

        self.server.start()

    def get_state(self):
        pass
