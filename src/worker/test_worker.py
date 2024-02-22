from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import vid_vec_rep_resnet
import json
from datetime import datetime
from core.models.media import MediaType
log = Logger(__name__)

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

def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        file_content = json.loads(body)
        video_path = {"path": rf"{file_content['path']}"}
        try:
            print("Processing File:", video_path)
            video_vec = vid_vec_rep_resnet.run(video_path)
            doc = generate_document(video_path["path"], video_vec)
            media_type = MediaType.VIDEO
            result = feluda.store.store(media_type, doc)
            print(result)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error indexing media", e)
            # requeue the media file
            ch.basic_nack(delivery_tag=method.delivery_tag)
    return worker

try:
    feluda = Feluda("config-indexer.yml")
    feluda.setup()
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    vid_vec_rep_resnet.initialize(param=None)
    feluda.queue.listen("tattle-search-index-queue", indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer")
