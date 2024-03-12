from core.feluda import ComponentType, Feluda
from core.logger import Logger
log = Logger(__name__)
from time import sleep

try:
    feluda = Feluda("worker/hash/config.yml")
    feluda.setup()
    count_queue = feluda.config.queue.parameters.queues[0]['name']
    feluda.start_component(ComponentType.QUEUE)

    for _ in range(5):
        dummy_payload = {
            "id": str(12345),
            "path": 'https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4'
        }
        feluda.queue.message(count_queue, dummy_payload)
        sleep(0.1)

except Exception as e:
    print("Error Initializing Indexer", e)