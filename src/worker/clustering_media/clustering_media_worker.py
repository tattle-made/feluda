from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import audio_vec_embedding_clap
from core.operators import cluster_embeddings
from core.operators import dimension_reduction
import json
from core.models.media_factory import AudioFactory
from time import sleep
import numpy as np
import binascii

log = Logger(__name__)


def make_report_indexed(clustering_results_json,dim_reduction_results_json, status):
    report = {}
    report["indexer_id"] = 1
    #report["post_id"] = data["id"]
    #report["media_type"] = data["media_type"]
    report["clustering_results"] = clustering_results_json
    report["dim_reduction_results"] = dim_reduction_results_json
    report["status"] = status
    report["status_code"] = 200
    return json.dumps(report)

def make_report_failed(media_type, status, file_id=None):
    report = {}
    report["indexer_id"] = 1
    # report["post_id"] = data["id"]
    report["media_type"] = media_type
    report["file_id"] = file_id if file_id else "unknown"
    report["status"] = status
    report["status_code"] = 400
    return json.dumps(report)

def make_report_failed_unsupported_media_type(media_type, status, file_id=None):
    report = {}
    report["indexer_id"] = 1
    #report["post_id"] = data["id"]
    report["media_type"] = media_type
    report["file_id"] = file_id if file_id else "unknown"
    report["clustering_results"] = None
    report["dim_reduction_results"] = None
    report["status"] = status
    report["status_code"] = 415  # 415 Unsupported Media Type
    return json.dumps(report)


def calc_audio_vec_crc(audio_vector):
    vec_arr = np.asarray(audio_vector)
    arr_crc = binascii.crc32(vec_arr.tobytes(order="C"))
    return arr_crc


def clustering_worker(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")
        audio_vec_crc = None
        file_list = json.loads(body)
        audio_embeddings = []

        for file in file_list:
            file_id = file["id"]
            file_path = file["path"]
            media_type = file["media_type"]

            if media_type == "audio":
                log.info("Media Type is Audio")
                try:
                    # download the audio from url (supports s3)
                    audio_path = AudioFactory.make_from_url(file_path)
                    # extract audio vectors
                    audio_vec = audio_vec_embedding_clap.run(audio_path)
                    audio_embeddings.append({"payload": file_id, "embedding": audio_vec})

                    # add crc to database
                    if feluda.config.store and "postgresql" in feluda.store:
                        audio_vec_crc = calc_audio_vec_crc(audio_vec)
                        feluda.store["postgresql"].store(
                            str(audio_vec_crc), "audio_vector_crc"
                            )
                        log.info("Audio CRC value added to PostgreSQL")
                        
                    # Add code to store in ES
                    
                except Exception as e:
                    print("Error in generating embeddings", e)
                    # send failed report to report queue
                    report = make_report_failed(media_type, "failed", file_id)
                    feluda.queue.message(
                    feluda.config.queue.parameters.queues[1]["name"], report
                    )
                    # requeue the media file
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            elif media_type == "video":
                pass
            
            else:
                log.info("This media type is not supported currently")
                report = make_report_failed_unsupported_media_type(media_type, "failed", file_id)
                feluda.queue.message(
                    feluda.config.queue.parameters.queues[1]["name"], report
                    )
                ch.basic_ack(delivery_tag=method.delivery_tag)

        clustering_results_json = cluster_embeddings.run(input_data=audio_embeddings, n_clusters=2, modality='audio')
        dim_reduction_results_json = dimension_reduction.perform_reduction(audio_embeddings)
        report = make_report_indexed(clustering_results_json, dim_reduction_results_json, "indexed")
        feluda.queue.message(
            feluda.config.queue.parameters.queues[1]["name"], report
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
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
clustering_media_index_queue = None
try:
    # Init Feluda and load config
    feluda = Feluda("worker/clustering_media/config.yml")
    feluda.setup()
    clustering_media_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    # setup Components
    feluda.start_component(ComponentType.QUEUE)
    if feluda.config.store:
        feluda.start_component(ComponentType.STORE)

    # init all operators
    audio_vec_embedding_clap.initialize(param={})
    cluster_embeddings.initialize(param={})
    dimension_reduction.setup_reduction(model_type='tsne', params={})

    # start listening to the queue
    feluda.queue.listen(clustering_media_index_queue, clustering_worker(feluda))
except Exception as e:
    print("Error Initializing Indexer", e)
    # Try connecting to Queue again
    retries = 0
    max_retries = 10
    handle_exception(
        feluda,
        clustering_media_index_queue,
        clustering_worker(feluda),
        retries,
        max_retries,
    )