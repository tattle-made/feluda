from core.feluda import ComponentType, Feluda
from core.logger import Logger
log = Logger(__name__)
from time import sleep

try:
    feluda = Feluda("config-indexer.yml")
    feluda.setup()
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)

    # while True:
    dummy_payload = {
        "id": str(12345),
        "path": 'tests/sample_data/sample-cat-video.mp4'
    }
    feluda.queue.message("tattle-search-index-queue", dummy_payload)
        # sleep(2)
except Exception as e:
    print("Error Initializing Indexer")



   