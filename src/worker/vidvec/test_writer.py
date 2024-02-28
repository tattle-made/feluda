from core.feluda import ComponentType, Feluda
from core.logger import Logger
log = Logger(__name__)
from time import sleep

try:
    feluda = Feluda("config-indexer.yml")
    feluda.setup()
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)

    for _ in range(10):
        dummy_payload = {
            "id": str(12345),
            "path": 'https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4'
        }
        feluda.queue.message("tattle-search-index-queue", dummy_payload)
        sleep(0.3)

except Exception as e:
    print("Error Initializing Indexer", e)