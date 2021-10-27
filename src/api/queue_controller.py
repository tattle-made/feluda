from core.config import QueueConfig
from core.rabbit_mq import RabbitMQ
from os import environ


class Queue:
    def __init__(self, param: QueueConfig):
        try:
            self.queue = RabbitMQ(
                {
                    "host": param.parameters.host_name,
                    "username": environ.get("MQ_USERNAME"),
                    "password": environ.get("MQ_PASSWORD"),
                }
            )
        except Exception:
            print("Error : Invalid params passed to RabbitMQ")
            raise TypeError("Invalid params passed to RabbitMQ")

    def connect(self):
        self.queue.connect()

    def declare_queues(self):
        self.queue.channel.queue_declare(
            queue="tattle-search-index-queue", durable=True
        )
        self.queue.channel.queue_declare(
            queue="tattle-search-report-queue", durable=True
        )

    def add_data_to_index_queue(self, payload):
        self.queue.publish_to_queue(
            queue_name="tattle-search-index-queue", payload=payload
        )

    def add_data_to_report_queue(self, payload):
        self.queue.publish_to_queue(
            queue_name="tattle-search-report-queue", payload=payload
        )

    def start_consuming(self, queue_name, callback):
        self.queue.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print(" [*] Waiting for messages. To exit press CTRL+C ")
        self.queue.channel.start_consuming()
