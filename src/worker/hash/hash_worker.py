from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import media_file_hash
import json
from core.models.media_factory import VideoFactory, AudioFactory
from time import sleep

log = Logger(__name__)


def make_report_indexed(data, status, hash_value=None):
    report = {}
    report["indexer_id"] = 1
    report["post_id"] = data["id"]
    report["media_type"] = data["media_type"]
    if hash_value is not None:
        report["hash_value"] = hash_value
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
        video_hash_value = None
        audio_hash_value = None
        file_content = json.loads(body)
        file_media_type = file_content["media_type"]
        if file_media_type == "video":
            log.info("Media Type is Video")
            try:
                # download the video from url (supports s3)
                video_path = VideoFactory.make_from_url(file_content["path"])
                # extrach hash value
                video_hash_value = media_file_hash.run(video_path)
                log.info(video_hash_value)
                # add hash value to database
                if feluda.config.store and "postgresql" in feluda.store:
                    feluda.store["postgresql"].store(
                        str(video_hash_value), "blake2b_hash_value"
                    )
                    log.info("Hash value added to PostgreSQL")
                # send indexed report to report queue
                report = make_report_indexed(file_content, "indexed", video_hash_value)
                feluda.queue.message(
                    feluda.config.queue.parameters.queues[1]["name"], report
                )
                # send ack
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print("Error indexing media", e)
                # send failed report to report queue
                report = make_report_failed(file_content, "failed")
                feluda.queue.message(
                    feluda.config.queue.parameters.queues[1]["name"], report
                )
                # requeue the media file
                ch.basic_ack(delivery_tag=method.delivery_tag)
        elif file_media_type == "audio":
            log.info("Media Type is Audio")
            try:
                # download audio file from url (supports S3)
                audio_path = AudioFactory.make_from_url(file_content["path"])
                # extrach hash value
                audio_hash_value = media_file_hash.run(audio_path)
                log.info(audio_hash_value)
                # add hash value to database
                if feluda.config.store and "postgresql" in feluda.store:
                    feluda.store["postgresql"].store(
                        str(audio_hash_value), "blake2b_hash_value"
                    )
                    log.info("Hash value added to PostgreSQL")
                # send indexed report to report queue
                report = make_report_indexed(file_content, "indexed", audio_hash_value)
                feluda.queue.message(
                    feluda.config.queue.parameters.queues[1]["name"], report
                )
                # send ack
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print("Error indexing media", e)
                # send failed report to report queue
                report = make_report_failed(file_content, "failed")
                feluda.queue.message(
                    feluda.config.queue.parameters.queues[1]["name"], report
                )
                # requeue the media file
                ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            log.info("This media type is not supported currently")
            # TODO: send a customised report and then report it to the queue with a ack
            report = make_report_failed(file_content, "failed")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[1]["name"], report
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

    return worker


feluda = None
count_queue = None
try:
    # Init Feluda and load config
    feluda = Feluda("worker/hash/config.yml")
    feluda.setup()
    count_queue = feluda.config.queue.parameters.queues[0]["name"]
    # setup Components
    if feluda.config.store:
        feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)
    # init hash operator
    media_file_hash.initialize(param=None)
    # start listening to the queue
    feluda.queue.listen(count_queue, indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    # Try connecting to Queue again
    retries = 0
    max_retries = 10
    handle_exception(feluda, count_queue, indexer(feluda), retries, max_retries)
