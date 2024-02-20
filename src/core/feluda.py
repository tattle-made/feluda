import logging

log = logging.getLogger(__name__)

from core import config, store
from core.server import Server
from core.operators import Operator
from core.queue import Queue
from enum import Enum


class ComponentType(Enum):
    OPERATORS = "operators"
    STORE = "store"
    QUEUE = "queue"
    SERVER = "server"


class Feluda:
    def __init__(self, configPath):
        self.config = config.load(configPath)
        if self.config.operators:
            self.operators = Operator(self.config.operators)
        if self.config.store:
            self.store = store.get_store(self.config.store)
        if self.config.queue:
            # print("---> 1", self.config.queue)
            self.queue = Queue.make(self.config.queue)
        if self.config.server:
            self.server = Server(self.config.server)

    def set_endpoints(self, endpoints):
        if self.server:
            for endpoint in endpoints:
                self.server.add_endpoint(endpoint(self))

            self.server.enable_endpoints()
        else:
            raise Exception("Server is not Configured")

    def start(self):
        if self.store:
            self.store.connect()
            self.store.optionally_create_index()

        if self.queue:
            self.queue.connect()

        if self.server:
            self.server.start()

    def start_component(self, component_type: ComponentType):
        if component_type == ComponentType.SERVER and self.server:
            self.server.start()
        elif component_type == ComponentType.STORE and self.store:
            self.store.connect()
            self.store.optionally_create_index()
        elif component_type == ComponentType.QUEUE and self.queue:
            self.queue.connect()
            self.queue.initialize()
        else:
            raise Exception("Unsupported Component Type")

    def get_state(self):
        pass
