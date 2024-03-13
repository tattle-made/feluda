"""
Documentation goes here
"""


def initialize(param):
    global imagehash

    import imagehash


def run(image):
    return str(imagehash.average_hash(image["image"]))


def cleanup(param):
    pass


def state():
    pass
