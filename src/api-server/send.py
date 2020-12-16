import pika
from os import environ
import json
import uuid
import sys
from controllers.queue_controller import queue_controller

def add_job_to_queue(payload):
    queue_controller.add_data_to_index_queue(payload=payload)