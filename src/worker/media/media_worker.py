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
    report["media_type"] = data["media_type"]
    report["status"] = status
    report["status_code"] = 200
    return json.dumps(report)

def make_report_failed(data, status):
    report = {}
    report["indexer_id"] = 1
    report["post_id"] = data["id"]
    report["media_type"] = data["media_type"]
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

def calc_video_vec_crc(video_vec_gen):
    count = 0
    combined_vec = [[]]
    for vector in video_vec_gen:
        if count == 0:
            # skip first vector - mean of keyframes
            count += 1
        else:
            combined_vec.append(vector["vid_vec"])
    # remove first list which is empty
    combined_vec = combined_vec[1:]
    combined_vec_arr = np.asarray(combined_vec)
    arr_crc = binascii.crc32(combined_vec_arr.tobytes(order='C'))
    return arr_crc

def indexer(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        file_content = json.loads(body)
        media_type = file_content["media_type"]
        if media_type == "video":
            try:
                # download the video from url (supports s3)
                video_path = VideoFactory.make_from_url(file_content["path"])
                # extract video vectors
                video_vec = vid_vec_rep_resnet.run(video_path)
                # add crc to database
                if feluda.config.postgresql:
                    video_vec_crc = calc_video_vec_crc(video_vec)
                    pg_manager.store(
                        "user_message_inbox_perceptually_similar",
                        str(video_vec_crc),
                        "video_vector_crc")
                    log.info("CRC value added to PostgreSQL")
                # generate document to report
                doc = generate_document(video_path["path"], video_vec)
                media_type = MediaType.VIDEO
                # store in ES
                if feluda.config.store:
                    result = feluda.store.store(media_type, doc)
                    log.info(result)
                # send indexed report to report queue
                report = make_report_indexed(file_content, "indexed")
                feluda.queue.message(feluda.config.queue.parameters.queues[1]["name"], report)
                # send ack
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print("Error indexing media", e)
                # send failed report to report queue
                report = make_report_failed(file_content, "failed")
                feluda.queue.message(feluda.config.queue.parameters.queues[1]["name"], report)
                # requeue the media file
                ch.basic_nack(delivery_tag=method.delivery_tag)
        elif media_type == "audio":
            pass
        else:
            log.info("This media type is not supported currently")
            # TODO: send a customised report and then report it to the queue with a ack

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
    # Init Feluda and load config
    feluda = Feluda("worker/media/config.yml")
    feluda.setup()
    # check if postgresql exists in config
    if feluda.config.postgresql:
        pg_manager = PostgreSQLManager()
        pg_manager.connect()
        pg_manager.create_trigger_function()
        pg_manager.create_table("user_message_inbox_perceptually_similar")
        pg_manager.create_trigger("user_message_inbox_perceptually_similar")
    else:
        log.info("PostgreSQL is not defined in the config file")
    media_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    # start components and init operators
    feluda.start_component(ComponentType.QUEUE)
    # check if store is present in config
    if feluda.config.store:
        feluda.start_component(ComponentType.STORE)
    else:
        log.info("Store (ES) is not defined in the config file")
    # start listening to the queue
    feluda.queue.listen(media_index_queue, indexer(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    # Try connecting to Queue again
    retries = 0
    max_retries = 10
    handle_exception(feluda, media_index_queue, indexer(feluda), retries, max_retries)
    if feluda.config.postgresql:
        pg_manager.close_connection()
