from api import components


store = None


def initialize(param, logger):
    """
    Exhaustive documentation on param can be found in docs/api/configuration
    todo : initialize elasticsearch indices if they aren't already configured.
    """
    # assign store to mongo, sql or es based on param
    # todo : validate param
    global store
    store_type = param["type"]

    if store_type is "es":
        from components.store import es

        store = es
    else:
        raise "Unsupported store type"


def run():
    pass
