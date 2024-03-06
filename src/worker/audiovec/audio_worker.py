from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import audio_vec_embedding
import json
from datetime import datetime
from core.models.media import MediaType
from core.models.media_factory import AudioFactory
from time import sleep
from datetime import datetime
log = Logger(__name__)

def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        file_content = json.loads(body)
        audio_path = AudioFactory.make_from_url(file_content['path'])
        try:
            media_type = MediaType.AUDIO
            audio_vec = audio_vec_embedding.run(audio_path)
            doc = {
            "e_kosh_id": str(1231231),
            "dataset": "test-dataset-id",
            "metadata": {},
            "audio_vec": audio_vec,
            "date_added": datetime.utcnow(),
            }
            # result = feluda.store.store(media_type, doc)
            # print(result)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error indexing media", e)
            # requeue the media file
            ch.basic_nack(delivery_tag=method.delivery_tag)
    return worker

def handle_exception(feluda, queue_name, worker_func, retries, max_retries):
    retry_interval = 60
    if retries < max_retries:
        print("Inside Handle Exception")
        try:
            feluda.start_component(ComponentType.QUEUE)
            feluda.queue.listen(queue_name, worker_func)
            return
        except Exception as e:
            print("Error handling exception:", e)
            retries = retries + 1
            sleep(retry_interval)
            handle_exception(feluda, queue_name, worker_func, retries, max_retries)
    else:
        print("Failed to re-establish connection after maximum retries.")

try:
    feluda = Feluda("worker/audiovec/config.yml")
    feluda.setup()
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    audio_vec_embedding.initialize(param=None)
    feluda.queue.listen("tattle-search-index-queue", indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    retries = 0
    max_retries = 10
    handle_exception(feluda, "tattle-search-index-queue", indexer(feluda), retries, max_retries)