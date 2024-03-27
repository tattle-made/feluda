from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import vid_vec_rep_resnet
from core.operators import audio_vec_embedding
import json
from datetime import datetime
from core.models.media import MediaType
from core.models.media_factory import VideoFactory
from core.models.media_factory import AudioFactory
from core.store.postgresql import PostgreSQLManager
from time import sleep
import numpy as np
import binascii

log = Logger(__name__)


def make_report_indexed(data, status):
    report = {}
    report["indexer_id"] = 1
    report["post_id"] = data["id"]
    report["status"] = status
    report["status_code"] = 200
    return json.dumps(report)


def make_report_failed(data, status):
    report = {}
    report["indexer_id"] = 1
    report["post_id"] = data["id"]
    report["status"] = status
    report["status_code"] = 400
    return json.dumps(report)

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
        media_type = file_content["media_type"]
        print(media_type)
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

feluda = None
pg_manager = None
media_index_queue = None
try:
    feluda = Feluda("worker/media/config.yml")
    feluda.setup()
    # pg_manager = PostgreSQLManager()
    # pg_manager.connect()
    # pg_manager.create_trigger_function()
    # pg_manager.create_table("user_message_inbox_perceptually_similar")
    # pg_manager.create_trigger("user_message_inbox_perceptually_similar")
    media_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    print(media_index_queue)
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    vid_vec_rep_resnet.initialize(param=None)
    audio_vec_embedding.initialize(param=None)
    feluda.queue.listen(media_index_queue, indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    retries = 0
    max_retries = 10
    handle_exception(feluda, media_index_queue, indexer(feluda), retries, max_retries)
    pg_manager.close_connection()