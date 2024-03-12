from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import audio_vec_embedding
import json
from core.models.media_factory import AudioFactory
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


def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        file_content = json.loads(body)
        audio_path = AudioFactory.make_from_url(file_content["path"])
        try:
            log.info("Processsing File")
            audio_vec = audio_vec_embedding.run(audio_path)
            search_result = feluda.store.find("audio", audio_vec)
            log.info(search_result)
            report = make_report_indexed(file_content, "searched")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[3]["name"], report
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print("Error indexing media", e)
            # requeue the media file
            report = make_report_failed(file_content, "failed")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[3]["name"], report
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


try:
    feluda = Feluda("worker/audiovec/config.yml")
    feluda.setup()
    audio_search_queue = feluda.config.queue.parameters.queues[2]["name"]
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    audio_vec_embedding.initialize(param=None)
    feluda.queue.listen(audio_search_queue, indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    retries = 0
    max_retries = 10
    handle_exception(feluda, audio_search_queue, indexer(feluda), retries, max_retries)
