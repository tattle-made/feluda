import logging
from . import rabbit_mq
from . import amazon_mq
from core.config import QueueConfig

# from os import environ

log = logging.getLogger(__name__)

queues = {"rabbitmq": rabbit_mq.RabbitMQ, "amazonmq": amazon_mq.AmazonMQ}


class Queue:
    def __init__(self):
        pass

    @staticmethod
    def make(param: QueueConfig):
        try:
            queue = queues[param.type](param)
            return queue
        except Exception:
            log.exception("Invalid params")
            print("Error : Invalid params passed to Queue")
            raise TypeError("Invalid params passed to Queue")

    # def connect(self):
    #     self.queue.connect()

    # def add_data_to_index_queue(self, payload):
    #     self.queue.publish_to_queue(
    #         queue_name="tattle-search-index-queue", payload=payload
    #     )

    # def add_data_to_report_queue(self, payload):
    #     self.queue.publish_to_queue(
    #         queue_name="tattle-search-report-queue", payload=payload
    #     )
