from core.store.es_vec import ES
from core.config import StoreConfig, StoreParameters
import time
import numpy as np
from locust import User, task, events, constant_throughput


class BenchmarkUser(User):
    wait_time = constant_throughput(1)

    def __init__(self, environment):
        super().__init__(environment)

        param_dict = {
            "host_name": "es",
            "text_index_name": "text",
            "image_index_name": "image",
            "video_index_name": "video",
            "audio_index_name": "audio",
        }

        self.param = StoreConfig(
            label="test",
            type="es",
            parameters=StoreParameters(
                host_name=param_dict["host_name"],
                image_index_name=param_dict["image_index_name"],
                text_index_name=param_dict["text_index_name"],
                video_index_name=param_dict["video_index_name"],
                audio_index_name=param_dict["audio_index_name"],
            ),
        )

    @task
    def search_video_vector(self):
        start_time = time.time()
        es = ES(self.param)
        es.connect()
        es.optionally_create_index()

        # Create random vector for benchmarking
        average_vector = np.random.randn(512).tolist()

        result = es.find("video", average_vector)

        total_time = int((time.time() - start_time) * 1000)
        # Register custom request event for stats
        events.request.fire(
            request_type="POST",
            name="Search",
            response_time=total_time,
            response_length=len(result),
        )
