from core.feluda import ComponentType, Feluda
from core.logger import Logger
from core.operators import audio_vec_embedding_clap
from core.operators import vid_vec_rep_clip, classify_video_zero_shot
from core.operators import cluster_embeddings, dimension_reduction
import requests
import json
from core.models.media_factory import AudioFactory, VideoFactory
from time import sleep

log = Logger(__name__)

def make_report_indexed(clustering_results_json, dim_reduction_results_json, status):
    report = {}
    report["clustering_results"] = clustering_results_json
    report["dim_reduction_results"] = dim_reduction_results_json
    report["status"] = status
    report["status_code"] = 200
    return json.dumps(report)

def make_report_failed(media_type, status, file_id=None):
    report = {}
    report["media_type"] = media_type
    report["file_id"] = file_id if file_id else "unknown"
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

def clustering_worker(feluda):
    def worker(ch, method, properties, body):
        print("MESSAGE RECEIVED")

        # Parse payload:
        input_payload = json.loads(body)
        json_path = input_payload["path"]
        video_config = input_payload["video"]
        audio_config = input_payload["audio"]

        # Fetch the file list:
        response = requests.get(json_path)
        file_list = response.json()

        audio_embeddings = []
        video_embeddings = []
        video_classifications = {}

        log.info("Processing files")
        for file in file_list:
            file_id = file["id"]
            file_path = file["path"]
            media_type = file["media_type"]

            if media_type == "audio":
                try:
                    # download the audio from url (supports s3)
                    audio_path = AudioFactory.make_from_url(file_path)
                    # extract audio vectors
                    audio_vec = audio_vec_embedding_clap.run(audio_path)
                    audio_embeddings.append({"payload": file_id, "embedding": audio_vec})

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
                try:
                    # download the video from url (supports s3)
                    video_path = VideoFactory.make_from_url(file_path)
                    if "labels" in video_config:
                        # run the zero-shot classifier:
                        pred = classify_video_zero_shot.run(video_path, video_config["labels"])["prediction"]
                        if pred not in video_classifications:
                            video_classifications[pred] = []
                        video_classifications[pred].append(file_id)
                        if video_config.get("tsne"):
                            embedding = vid_vec_rep_clip.run(video_path)
                            video_embeddings.append({
                                "embedding": next(embedding)["vid_vec"],
                                "payload": file_id
                            })
                    else:
                        embedding = vid_vec_rep_clip.run(video_path)
                        video_embeddings.append({
                            "embedding": next(embedding)["vid_vec"],
                            "payload": file_id
                        })

                except Exception as e:
                    print("Error in generating embeddings", e)
                    # send failed report to report queue
                    report = make_report_failed(media_type, "failed", file_id)
                    feluda.queue.message(
                        feluda.config.queue.parameters.queues[1]["name"], report
                    )
                    # requeue the media file
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                pass

        log.info("Clustering embeddings")
        try:
            clustering_results_audio = cluster_embeddings.run(input_data=audio_embeddings, n_clusters=audio_config.get("n_clusters"), modality='audio')
            if "labels" in video_config:
                clustering_results_video = video_classifications
            else:
                clustering_results_video = cluster_embeddings.run(input_data=video_embeddings, n_clusters=video_config.get("n_clusters"), modality='video')
                clustering_results_json = {
                    "audio": clustering_results_audio,
                    "video": clustering_results_video
                    }
        except Exception as e:
            print("Error in clustering:", e)
            report = make_report_failed("clustering", "failed")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[1]["name"], report
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        log.info("Calculating t-SNE co-ordinates")
        try:
            dim_reduction_results_audio = None
            dim_reduction_results_video = None
            if audio_config.get("tsne"):
                dim_reduction_results_audio = dimension_reduction.run(audio_embeddings)
            if video_config.get("tsne"):
                dim_reduction_results_video = dimension_reduction.run(video_embeddings)
            
            dim_reduction_results_json = {
                "audio": dim_reduction_results_audio,
                "video": dim_reduction_results_video
                }
        except Exception as e:
            print("Error in dimension reduction:", e)
            report = make_report_failed("dimension reduction", "failed")
            feluda.queue.message(
                feluda.config.queue.parameters.queues[1]["name"], report
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        report = make_report_indexed(clustering_results_json, dim_reduction_results_json, "indexed")
        log.info("Report generated")
        feluda.queue.message(
            feluda.config.queue.parameters.queues[1]["name"], report
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    return worker

feluda = None
clustering_media_index_queue = None
try:
    # Init Feluda and load config
    feluda = Feluda("worker/clustering_media/config.yml")
    feluda.setup()
    clustering_media_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    # setup Components
    feluda.start_component(ComponentType.QUEUE)

    # init all operators
    audio_vec_embedding_clap.initialize(param={})
    vid_vec_rep_clip.initialize(param={})
    classify_video_zero_shot.initialize(param={})
    cluster_embeddings.initialize(param={})
    dimension_reduction.initialize(params={"perplexity": 5})

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