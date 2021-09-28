from flask import Flask


class Server:
    def __init__(self, param, controllers, log) -> None:
        self.controllers = controllers
        self.app = Flask(__name__)
        self.setup_routes()
        pass

    def setup_routes(self):
        print("setting up routes")
        for controller in self.controllers:
            routes = controller.get_routes()
            handler = controller.get_handler()
            for route in routes:
                endpoint, method_type = route
                self.app.add_url_rule(endpoint, handler)

    def start(self):
        @self.app.route("/")
        def hello_world():
            return "<p>Hello, World!</p>"

        self.app.run(port=5000)
    