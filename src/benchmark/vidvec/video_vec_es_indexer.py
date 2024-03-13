from core.store.es_vec import ES
from core.config import StoreConfig, StoreParameters
from core.models.media import MediaType
from core.operators import vid_vec_rep_resnet
from datetime import datetime
import time
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

param = None


def initialize():
    param_dict = {
        "host_name": "es",
        "text_index_name": "text",
        "image_index_name": "image",
        "video_index_name": "video",
        "audio_index_name": "audio",
    }

    global param

    param = StoreConfig(
        label="test",
        type="es",
        parameters=StoreParameters(
            host_name=param_dict["host_name"],
            image_index_name=param_dict["image_index_name"],
            text_index_name=param_dict["text_index_name"],
            video_index_name=param_dict["video_index_name"],
            audio_index_name=param_dict["audio_index_name"],
        ),
    )


def generate_document(post_id: str, representation: any):
    base_doc = {
        "e_kosh_id": "",
        "dataset": post_id,
        "metadata": None,
        "date_added": datetime.now().isoformat(),
    }

    def generator_doc():
        for vector in representation:
            base_doc["_index"] = "video"
            base_doc["vid_vec"] = vector["vid_vec"]
            base_doc["is_avg"] = vector["is_avg"]
            base_doc["duration"] = vector["duration"]
            base_doc["n_keyframes"] = vector["n_keyframes"]
            yield base_doc

    return generator_doc


def store_video_vector():
    es = ES(param)
    es.connect()

    media_type = MediaType.VIDEO
    vid_vec_rep_resnet.initialize(param=None)

    folder_path = r"core/operators/sample_data/video_files"
    count = 0
    start_time = time.time()
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        video = {"path": file_path}
        embedding = vid_vec_rep_resnet.run(video)
        doc = generate_document(file_name, embedding)
        # TODO: save doc to storage so we don't have to recompute embeddings again
        es.store(media_type, doc)
        count += 1
        print("Indexed file:", count)
        # print("result:", result)
    end_time = time.time()
    duration = end_time - start_time
    print("Time taken:", duration)
    print("Files indexed:", count)


if __name__ == "__main__":
    initialize()
    store_video_vector()
