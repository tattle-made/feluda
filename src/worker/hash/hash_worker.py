from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import media_file_hash
import json
from core.models.media_factory import VideoFactory
from core.store.postgresql import PostgreSQLManager
from time import sleep
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

def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        file_content = json.loads(body)
        video_path = VideoFactory.make_from_url(file_content['path'])
        try:
            log.info("Processing file")
            hash = media_file_hash.run(video_path)
            log.debug(hash)
            pg_manager.store("user_message_inbox_duplicate", str(hash), "blake2b_hash_value")
            log.info("Hash value added to PostgreSQL")
            report = make_report_indexed(file_content, "indexed")
            feluda.queue.message(feluda.config.queue.parameters.queues[1]['name'], report)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error indexing media", e)
            report = make_report_failed(file_content, "failed")
            feluda.queue.message(feluda.config.queue.parameters.queues[1]['name'], report)
            # requeue the media file
            ch.basic_nack(delivery_tag=method.delivery_tag)
    return worker

feluda = None
pg_manager = None
count_queue = None
try:
    feluda = Feluda("worker/hash/config.yml")
    feluda.setup()
    pg_manager = PostgreSQLManager()
    pg_manager.connect()
    pg_manager.create_trigger_function()
    pg_manager.create_table("user_message_inbox_duplicate")
    pg_manager.create_trigger("user_message_inbox_duplicate")
    count_queue = feluda.config.queue.parameters.queues[0]['name']
    feluda.start_component(ComponentType.QUEUE)
    media_file_hash.initialize(param=None)
    feluda.queue.listen(count_queue, indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    retries = 0
    max_retries = 10
    handle_exception(feluda, count_queue, indexer(feluda), retries, max_retries)
    pg_manager.close_connection()