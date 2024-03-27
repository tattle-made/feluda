from core.feluda import ComponentType, Feluda
from core.logger import Logger
from time import sleep
import uuid
import sys

log = Logger(__name__)

try:
    feluda = Feluda("worker/media/config.yml")
    feluda.setup()
    media_index_queue = feluda.config.queue.parameters.queues[0]["name"]
    feluda.start_component(ComponentType.QUEUE)
    # take media_type from command line
    media_type = sys.argv[1] if len(sys.argv) > 1 else "video"
    media_paths = {
        "video": "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/sample-cat-video.mp4",
        "audio": "https://raw.githubusercontent.com/tattle-made/feluda/main/src/core/operators/sample_data/audio.wav",
    }
    path = media_paths.get(media_type)
    if path is None:
        raise ValueError("Unsupported media type")

    for _ in range(1):
        unique_id = str(uuid.uuid4())
        dummy_payload = {
            "id": unique_id,
            "path": path,
            "media_type": media_type,
        }
        feluda.queue.message(media_index_queue, dummy_payload)
        sleep(0.3)
except Exception as e:
    print("Error Sending Payload", e)
