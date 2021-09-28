# connect to queue
# start listening for messages
# process them

import logging
from datetime import datetime
import sys
import os
from os import environ
import pika
import json
from dotenv import load_dotenv

load_dotenv()
from helper import index_data
from time import perf_counter
from services.es import get_es_instance
from controllers.queue_controller import queue_controller
import logging

logger = logging.getLogger("tattle-api")

try:
    queue_controller.connect()
    queue_controller.declare_queues()
except Exception:
    logging.info(logging.traceback.format_exc())
    exit()

es = get_es_instance()


def callback(ch, method, properties, body):
    print("MESSAGE RECEIVED")
    start = perf_counter()
    data = json.loads(body)
    # print(data)
    report = {}
    report["source_id"] = data["source_id"]
    report["source"] = data.get("source", "tattle-admin")

    try:
        print("Indexing data ...")
        index_id = index_data(es, data)

        print("Sending report to queue ...")
        report["index_timestamp"] = str(datetime.utcnow())
        report["index_id"] = index_id
        report["status"] = "indexed"

        queue_controller.add_data_to_report_queue(json.dumps(report))
        delta = perf_counter() - start
        print("Time taken: ", delta)
        print("Indexing success report sent to report queue")
        print("")
        print("")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception:
        logging.info("Error indexing media")
        logging.info(logging.traceback.format_exc())
        print("Sending report to queue ...")
        report["status"] = "failed"
        report["failure_timestamp"] = str(datetime.utcnow())

        queue_controller.add_data_to_report_queue(json.dumps(report))
        print("Indexing failure report sent to report queue")
        try:
            os.remove("/tmp/vid.mp4")
        except:
            pass
        ch.basic_ack(delivery_tag=method.delivery_tag)


queue_controller.start_consuming("tattle-search-index-queue", callback)
