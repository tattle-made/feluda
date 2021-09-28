class HealthRequestModel:
    pass


class HealthRoute:
    def __init__(self):
        pass

    def handle_health(self, req):
        return "healthy"

    def make_handlers(self, req):
        if req.path is "/health":
            return self.handle_health(req)


class HealthController:
    def __init__(self):
        pass

    def get_routes(self):
        return [("/health", "GET")]

    def get_handler(self):
        route = HealthRoute()
        # return route.make_handlers(req)
        return "healthy"
