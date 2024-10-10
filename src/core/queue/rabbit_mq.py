import logging
from core.config import QueueConfig
import pika
import json
from os import environ

log = logging.getLogger(__name__)


class RabbitMQ:
    def __init__(self, param: QueueConfig):
        try:
            self.declared_queues = []
            self.mq_username = environ.get("MQ_USERNAME")
            self.mq_password = environ.get("MQ_PASSWORD")
            # self.mq_host = param.parameters.host_name
            self.mq_host = environ.get("MQ_HOST")
            self.queues = []
            for queue in param.parameters.queues:
                self.queues.append(queue)
        except Exception:
            print("Invalid parameter")
            raise TypeError("Invalid parameters passed to RabbitMQ")

    def connect(self):
        try:
            credentials = pika.PlainCredentials(self.mq_username, self.mq_password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.mq_host,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300,
                )
            )
            self.channel = connection.channel()
            self.channel.confirm_delivery()
            print("----> 2 ", "Success Connecting to RabbitMQ")

        except Exception:
            log.exception("Error Connecting to RabbitMQ")
            print("Error Connecting to RabbitMQ ")
            raise Exception("Error connecting to RabbitMQ")

    def initialize(self):
        for queue in self.queues:
            self.declare_queue(queue["name"])
            self.declared_queues.append(queue["name"])
            print("Queue Declared : ", queue)

    def is_connected(self):
        return self.channel.is_open

    def message(self, queue_name, payload):
        if self.is_connected():
            try:
                self.channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    ),  # make message persistent
                    body=json.dumps(payload),
                )
            except pika.exceptions.UnroutableError:
                print("Message could not be confirmed")
        else:
            self.connect()
            self.channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                properties=pika.BasicProperties(
                    delivery_mode=2
                ),  # make message persistent
                body=json.dumps(payload),
            )

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def listen(self, queue_name, callback):
        self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
        print(" [*] Waiting for messages. To exit press CTRL+C ")
        self.channel.start_consuming()

    def reset(self):
        for queue in self.queues:
            self.channel.queue_delete(queue=queue["name"])
        print("Queues Deleted")
