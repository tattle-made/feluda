import logging
from datetime import datetime
import sys
import os
from os import environ
import pika
import json
# from dotenv import load_dotenv
# load_dotenv()
from helper import index_data

credentials = pika.PlainCredentials(environ.get(
    'MQ_USERNAME'), environ.get('MQ_PASSWORD'))
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=environ.get('MQ_HOST'), credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='tattle-search-index-queue', durable=True)
channel.queue_declare(queue='tattle-search-report-queue', durable=True)


def callback(ch, method, properties, body):
    print("MESSAGE RECEIVED %r" % body)
    data = json.loads(body)
    print(data)
    report = {}
    report["source_id"] = data["source_id"]
    report["source"] = data["source"]

    try:
        print("Indexing data ...")
        index_id = index_data(data)

        print("Sending report to queue ...")
        report["index_timestamp"] = str(datetime.utcnow())
        report["index_id"] = index_id
        report["status"] = "indexed"

        channel.basic_publish(exchange='',
                                routing_key='tattle-search-report-queue',
                                properties=pika.BasicProperties(
                                    content_type='application/json',
                                    delivery_mode=2),  # make message persistent
                                body=json.dumps(report))

        print("Indexing success report sent to report queue")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception:
        print('Error indexing media ')
        print(logging.traceback.format_exc())
        print("Sending report to queue ...")
        report["status"] = "failed"
        report["failure_timestamp"] = str(datetime.utcnow())
        
        channel.basic_publish(exchange='',
            routing_key='tattle-search-report-queue',
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=2), # make message persistent
            body=json.dumps(report))
        print("Indexing failure report sent to report queue")
        try:
            os.remove('/tmp/vid.mp4')
        except:
            pass
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='tattle-search-index-queue',
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C ')
channel.start_consuming()