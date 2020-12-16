import pika
from os import environ
import json
import uuid
import sys
from controllers.queue_controller import queue_controller

# credentials = pika.PlainCredentials(environ.get(
#     'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(
#         host=environ.get('MQ_HOST'), 
#         credentials=credentials,
#         heartbeat=600,
#         blocked_connection_timeout=300))
# channel = connection.channel()

# channel.queue_declare(queue='tattle-search-index-queue', durable=True)
# channel.queue_declare(queue='tattle-search-report-queue', durable=True)
# channel.confirm_delivery()

def add_job_to_queue(payload):
    queue_controller.add_data_to_index_queue(payload=payload)