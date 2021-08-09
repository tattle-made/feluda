import config, index, ssearch, server, datastore, queue, logger


def initialize():
    """
    This is called early on during the app startup and will raise an Exception and exit if any of the essential components
    are'nt successfully initialized.
    """
    config.initialize()
    index.initialize(
        text=config.text_features,
        image=config.image_features,
        video=config.video_features,
    )
    # search.initialize()
    # server.initialize()
    # datastore.initialize()
    # queue.initialize()
    # logger.initialize()


def get_state(verbose=False):
    """
    Print the state of activation of all components in the app
    """
    state = []
    state.append(config.get_state())
    return state


def show_dependecies():
    pass
