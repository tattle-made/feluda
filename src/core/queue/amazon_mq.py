import ssl
import pika
import logging
import json
from core.config import QueueConfig
from os import environ

log = logging.getLogger(__name__)


class AmazonMQ:
    def __init__(self, param: QueueConfig):
        try:
            self.rabbitmq_user = environ.get("MQ_USERNAME")
            self.rabbitmq_password = environ.get("MQ_PASSWORD")
            self.rabbitmq_broker_id = environ.get("MQ_BROKER_ID")
            self.region = environ.get("MQ_REGION")
            self.queues = []
            for queue in param.parameters.queues:
                self.queues.append(queue["name"])
        except Exception:
            print("Invalid parameter")
            raise TypeError("Invalid parameters passed to AmazonMQ")

    def connect(self):
        try:
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")

            url = f"amqps://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_broker_id}.mq.{self.region}.amazonaws.com:5671"
            parameters = pika.URLParameters(url)
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            print("----> 2 ", "Success Connecting to AmazonMQ")
        except Exception:
            log.exception("Error Connecting to AmazonMQ")
            print("Error Connecting to AmazonMQ")
            raise Exception("Error connecting to AmazonMQ")

    def initialize(self):
        for queue_name in self.queues:
            self.channel.queue_declare(queue=queue_name)
            print("Queue Declared : ", queue_name)

    def is_connected(self):
        return self.channel.is_open

    def message(self, queue_name, payload):
        try:
            channel = self.connection.channel()
            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=json.dumps(payload),
            )
            print("Sent message")
        except Exception:
            log.exception("Error sending message")
            print("Error sending message")
            raise Exception("Error sending message")

    def listen(self, queue_name, callback):
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()
