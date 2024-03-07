from core.feluda import ComponentType, Feluda
from core.logger import Logger
log = Logger(__name__)
from time import sleep

try:
    feluda = Feluda("worker/audiovec/config.yml")
    feluda.setup()
    audio_index_queue = feluda.config.queue.parameters.queues[2]['name']
    feluda.start_component(ComponentType.STORE)
    feluda.start_component(ComponentType.QUEUE)

    for _ in range(1):
        dummy_payload = {
            "id": str(12345),
            "path": 'https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/audio.wav'
        }
        feluda.queue.message(audio_index_queue, dummy_payload)
        sleep(0.3)

except Exception as e:
    print("Error Initializing Indexer", e)