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
from core.queue.amazon_mq import AmazonMQ
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
    arr_crc = binascii.crc32(combined_vec_arr.tobytes(order="C"))
    return arr_crc


def calc_audio_vec_crc(audio_vector):
    vec_arr = np.asarray(audio_vector)
    arr_crc = binascii.crc32(vec_arr.tobytes(order="C"))
    return arr_crc


def indexer(feluda, amazom_queue_manager):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        global table_name
        file_content = json.loads(body)
        file_media_type = file_content["media_type"]
        if file_media_type == "video":
            log.info("Media Type is Video")
            try:
                # download the video from url (supports s3)
                video_path = VideoFactory.make_from_url(file_content["path"])
                # extract video vectors
                video_vec = vid_vec_rep_resnet.run(video_path)
                # add crc to database
                if feluda.config.postgresql:
                    video_vec_crc = calc_video_vec_crc(video_vec)
                    pg_manager.store(table_name, str(video_vec_crc), "video_vector_crc")
                    log.info("Video CRC value added to PostgreSQL")
                # generate document
                doc = generate_document(video_path["path"], video_vec)
                media_type = MediaType.VIDEO
                # store in ES
                if feluda.config.store:
                    result = feluda.store.store(media_type, doc)
                    log.info(result)
                # send indexed report to report queue
                report = make_report_indexed(file_content, "indexed")
                amazom_queue_manager.send_message(
                    feluda.config.amazon_queue.parameters.queues[1]["name"], report
                )
                # send ack
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print("Error indexing media", e)
                # send failed report to report queue
                report = make_report_failed(file_content, "failed")
                amazom_queue_manager.send_message(
                    feluda.config.amazon_queue.parameters.queues[1]["name"], report
                )
                # requeue the media file
                ch.basic_nack(delivery_tag=method.delivery_tag)
        elif file_media_type == "audio":
            log.info("Media Type is Audio")
            try:
                # download audio file from url (supports S3)
                audio_path = AudioFactory.make_from_url(file_content["path"])
                # generate audio vec
                audio_vec = audio_vec_embedding.run(audio_path)
                # add crc to database
                if feluda.config.postgresql:
                    audio_vec_crc = calc_audio_vec_crc(audio_vec)
                    pg_manager.store(table_name, str(audio_vec_crc), "audio_vector_crc")
                    log.info("Audio CRC value added to PostgreSQL")
                # generate document
                doc = {
                    "e_kosh_id": str(1231231),
                    "dataset": "test-dataset-id",
                    "metadata": {},
                    "audio_vec": audio_vec,
                    "date_added": datetime.utcnow(),
                }
                media_type = MediaType.AUDIO
                # store in ES
                if feluda.config.store:
                    result = feluda.store.store(media_type, doc)
                    log.info(result)
                # send indexed report to report queue
                report = make_report_indexed(file_content, "indexed")
                amazom_queue_manager.send_message(
                    feluda.config.amazon_queue.parameters.queues[1]["name"], report
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print("Error indexing media", e)
                # send failed report to report queue
                report = make_report_failed(file_content, "failed")
                amazom_queue_manager.send_message(
                    feluda.config.amazon_queue.parameters.queues[1]["name"], report
                )
                # requeue the media file
                ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            log.info("This media type is not supported currently")
            # TODO: send a customised report and then report it to the queue with a ack
            report = make_report_failed(file_content, "failed")
            amazom_queue_manager.send_message(
                feluda.config.amazon_queue.parameters.queues[1]["name"], report
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)

    return worker


def handle_exception(feluda, queue_name, worker_func, retries, max_retries):
    retry_interval = 60
    if retries < max_retries:
        print("Inside Handle Exception")
        try:
            amazom_queue_manager = AmazonMQ(queue_config)
            amazom_queue_manager.connect()
            amazom_queue_manager.create_queue()
            amazom_queue_manager.listen(queue_name, worker_func)
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
    queue_config = feluda.config.amazon_queue
    media_index_queue = queue_config.parameters.queues[0]["name"]
    # setup Amazon MQ
    amazom_queue_manager = AmazonMQ(queue_config)
    amazom_queue_manager.connect()
    amazom_queue_manager.create_queue()
    # check if postgresql exists in config
    if feluda.config.postgresql:
        pg_manager = PostgreSQLManager()
        pg_manager.connect()
        pg_manager.create_trigger_function()
        table_name = feluda.config.postgresql.parameters.table_names[0]["name"]
        pg_manager.create_table(table_name)
        pg_manager.create_trigger(table_name)
    else:
        log.info("PostgreSQL is not defined in the config file")
    # check if store is present in config and start component
    if feluda.config.store:
        feluda.start_component(ComponentType.STORE)
    else:
        log.info("Store (ES) is not defined in the config file")
    # init all operators
    vid_vec_rep_resnet.initialize(param=None)
    audio_vec_embedding.initialize(param=None)
    # start listening to the queue
    amazom_queue_manager.listen(
        media_index_queue, indexer(feluda, amazom_queue_manager)
    )
except Exception as e:
    print("Error Initializing Indexer", e)
    # Try connecting to Queue again
    retries = 0
    max_retries = 10
    handle_exception(
        feluda,
        media_index_queue,
        indexer(feluda, amazom_queue_manager),
        retries,
        max_retries,
    )
    if feluda.config.postgresql:
        pg_manager.close_connection()