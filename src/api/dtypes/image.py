import requests
import PIL
from io import BytesIO
import numpy as np
from datetime import datetime

# todo add details like file size, resolution etc?
# todo should functions have a lean version to use when you know what you are doing?


def make_from_url(image_url):
    resp = requests.get(image_url)
    image_bytes = resp.content
    image = PIL.Image.open(BytesIO(image_bytes))
    image_array = np.array(image)
    return {"image": image, "image_array": image_array, "image_bytes": image_bytes}


def make_from_file(image_path):
    with open(image_path, mode="rb") as file:
        image_bytes = file.read()
        image = PIL.Image.open(BytesIO(image_bytes))
        image_array = np.array(image)
        return {"image": image, "image_array": image_array, "image_bytes": image_bytes}


def make_for_store(store_type, post_data, post_metadata):
    if store_type is "es":
        return make_for_es()
    else:
        raise "Unsupported Store Type. Currently Supported Store Types : [es]. Instead found " + store_type


def make_for_es(rep, post_id, client_id, metadata):
    doc = {
        "source_id": str(post_id),
        "source": client_id if client_id is not None else "tattle-admin",
        "metadata": metadata,
        "image_vec": rep,
        "date_added": datetime.utcnow(),
    }
    return doc
