from core.feluda import ComponentType, Feluda
from core.logger import Logger
from time import sleep

log = Logger(__name__)

try:
    feluda = Feluda("worker/vidvec/config.yml")
    feluda.setup()
    video_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)

    for _ in range(10):
        dummy_payload = {
            "id": str(12345),
            "path": "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4",
        }
        feluda.queue.message(video_index_queue, dummy_payload)
        sleep(0.3)

except Exception as e:
    print("Error Initializing Indexer", e)
