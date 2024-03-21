from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import audio_vec_embedding
import json
from core.models.media import MediaType
from core.models.media_factory import AudioFactory
from core.store.postgresql import PostgreSQLManager
from time import sleep
from datetime import datetime
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


def indexer(feluda):

    def calc_audio_vec_crc(audio_vector):
        vec_arr = np.asarray(audio_vector)
        arr_crc = binascii.crc32(vec_arr.tobytes(order='C'))
        return arr_crc

    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        file_content = json.loads(body)
        audio_path = AudioFactory.make_from_url(file_content["path"])
        try:
            log.info("Processing File")
            media_type = MediaType.AUDIO
            audio_vec = audio_vec_embedding.run(audio_path)
            audio_vec_crc = calc_audio_vec_crc(audio_vec)
            log.debug("audio_vec_crc:{}".format(audio_vec_crc))
            # write the crc into a table
            pg_manager.store(
                "user_message_inbox_perceptually_similar",
                str(audio_vec_crc),
                "audio_vector_crc")
            log.info("CRC value added to PostgreSQL")
            doc = {
                "e_kosh_id": str(1231231),
                "dataset": "test-dataset-id",
                "metadata": {},
                "audio_vec": audio_vec,
                "date_added": datetime.utcnow(),
            }
            result = feluda.store.store(media_type, doc)
            log.info(result)
            report = make_report_indexed(file_content, "indexed")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[1]["name"], report
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error indexing media", e)
            # requeue the media file
            report = make_report_failed(file_content, "failed")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[1]["name"], report
            )
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


feluda = None
pg_manager = None
audio_index_queue = None
try:
    feluda = Feluda("worker/audiovec/config.yml")
    feluda.setup()
    pg_manager = PostgreSQLManager()
    pg_manager.connect()
    pg_manager.create_trigger_function()
    pg_manager.create_table("user_message_inbox_perceptually_similar")
    pg_manager.create_trigger("user_message_inbox_perceptually_similar")
    audio_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    audio_vec_embedding.initialize(param=None)
    feluda.queue.listen(audio_index_queue, indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    retries = 0
    max_retries = 10
    handle_exception(feluda, audio_index_queue, indexer(feluda), retries, max_retries)
    pg_manager.close_connection()
