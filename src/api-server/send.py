import pika
from os import environ
import json
import uuid
import sys

credentials = pika.PlainCredentials(environ.get(
    'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='tattle-search-index-queue', durable=True)
channel.queue_declare(queue='tattle-search-report-queue', durable=True)

def add_job_to_queue(payload):
    channel.basic_publish(
        exchange='', 
        routing_key='tattle-search-index-queue', 
        properties=pika.BasicProperties(delivery_mode=2), # make message persistent
        body=json.dumps(payload))
