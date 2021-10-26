import logging

log = logging.getLogger(__name__)
import pika
import json


class RabbitMQ:
    def __init__(self, param):
        try:
            self.mq_username = param["username"]
            self.mq_password = param["password"]
            self.mq_host = param["host"]
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
            print("Success Connecting to RabbitMQ")
            self.channel.confirm_delivery()
            print("Publisher confirms enabled")
        except Exception:
            print("Error Connecting to RabbitMQ ")
            raise Exception("Error connecting to RabbitMQ")

    def is_connected(self):
        return self.channel.is_open

    def publish_to_queue(self, queue_name, payload):
        if self.is_connected():
            try:
                self.channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    properties=pika.BasicProperties(
                        delivery_mode=2
                    ),  # make message persistent
                    body=json.dumps(payload),
                )
                print("Message published")
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
