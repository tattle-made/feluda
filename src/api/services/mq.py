from os import environ
import pika
import json
import logging

class MQ():
    def __init__(self):
        self.mq_username = environ.get('MQ_USERNAME')
        self.mq_password = environ.get('MQ_PASSWORD')
        self.mq_host = environ.get('MQ_HOST')

    def connect(self):
        try:
            credentials = pika.PlainCredentials(
                self.mq_username,
                self.mq_password)
            if self.mq_host == "localhost":
                connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.mq_host,
                    heartbeat=600,
                    blocked_connection_timeout=300
                ))
            else:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.mq_host,
                        credentials=credentials,
                        heartbeat=600,
                        blocked_connection_timeout=300
                    ))
            self.channel = connection.channel()
            print('Success Connecting to RabbitMQ')
            self.channel.confirm_delivery()
            print("Publisher confirms enabled")
        except Exception:
            print('Error Connecting to RabbitMQ ')
            print(logging.traceback.format_exc())

    def is_connected(self):
        return self.channel.is_open

    def publish_to_queue(self, queue_name, payload):
        if self.is_connected():
            try:
                self.channel.basic_publish(exchange='',
                                        routing_key=queue_name,
                                        properties=pika.BasicProperties(
                                            delivery_mode=2),  # make message persistent
                                        body=json.dumps(payload))
                print("Message published")
            except pika.exceptions.UnroutableError:
                print('Message could not be confirmed')
        else:
            self.connect()
            self.channel.basic_publish(exchange='',
                           routing_key=queue_name,
                           properties=pika.BasicProperties(
                               delivery_mode=2),  # make message persistent
                           body=json.dumps(payload))

mq = MQ()

def get_mq_instance():
    return mq
