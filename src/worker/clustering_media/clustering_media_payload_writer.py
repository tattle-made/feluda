from core.feluda import ComponentType, Feluda
from core.logger import Logger
log = Logger(__name__)

try:
    feluda = Feluda("worker/clustering_media/config.yml")
    feluda.setup()
    clustering_media_index_queue = feluda.config.queue.parameters.queues[0]['name']
    feluda.start_component(ComponentType.QUEUE)
    dummy_input = {
        "path": "https://raw.githubusercontent.com/aatmanvaidya/audio-files/main/clustering-media/media_payload.json",
        "video": {
            "n_clusters": 3,
            "tsne": True
        },
        "audio": {
            "n_clusters": 3,
            "tsne": True
        }
    }
    feluda.queue.message(clustering_media_index_queue, dummy_input)
except Exception as e:
    print("Error Initializing Indexer", e)
