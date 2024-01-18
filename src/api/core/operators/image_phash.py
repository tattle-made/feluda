from operators.installer import install_packages

"""
Documentation goes here
"""
requirement_list = ["ImageHash==4.2.1"]


def initialize(param):
    install_packages(requirement_list)

    global imagehash

    import imagehash


def run(image):
    return str(imagehash.average_hash(image["image"]))


def cleanup(param):
    pass


def state():
    pass
