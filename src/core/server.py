import logging

from core.config import ServerConfig

log = logging.getLogger(__name__)
from flask import Flask
from flask_cors import CORS


class Server:
    def __init__(self, param: ServerConfig) -> None:
        self.param = param
        self.app = Flask(__name__)
        CORS(self.app)
        self.endpoints = []

    def add_endpoint(self, endpoint):
        self.endpoints.append(endpoint)
        # self.setup_routes()

    def enable_endpoints(self):
        print("setting up routes")
        for endpoint in self.endpoints:
            routes = endpoint.get_routes()
            handler = endpoint.get_handler
            try:
                for route in routes:
                    endpoint, name, methods = route
                    self.app.add_url_rule(endpoint, name, handler, methods=methods)
            except Exception as e:
                log.exception("Could not add Route")

    def start(self):
        @self.app.route("/")
        def hello_world():
            return "<p>Hello, World!</p>"

        self.app.run(host="0.0.0.0", port=self.param.parameters.port, debug=True)
