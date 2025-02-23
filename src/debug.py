#!/usr/bin/env python

import click
from core.config import QueueConfig, QueueParameters, StoreConfig, StoreParameters
from core import store
from core.logger import Logger
from core.queue import Queue
import pika
import os

logger = Logger(__name__)

@click.group()
def cli():
    pass

@cli.command()
@click.option(
    "-s",
    "--service",
    type=click.Choice(["queue", "store"]),
    help="Enter service name. Options : queue or store",
    required=True,
)
def ping(service):
    print("ping", service)
    if service == "store":
        Store = store.get_store(
            StoreConfig(
                label="store",
                type="es_vec",
                parameters=StoreParameters(
                    host_name="192.46.212.142",
                    image_index_name="image",
                    video_index_name="video",
                    text_index_name="text",
                ),
            )
        )
        Store.connect()
        response = Store.ping()
        click.echo(response)
    elif service == "queue":
        queue = Queue.make(
            QueueConfig(
                label="Queue",
                type="rabbitmq",
                parameters=QueueParameters(
                    host_name="rabbitmq",
                    queues=[
                        {"name": "tattle-search-index-queue"},
                        {"name": "tattle-search-report-queue"},
                    ],
                ),
            )
        )
        queue.connect()

@cli.command()
@click.option(
    "-s",
    "--service",
    type=click.Choice(["queue", "store"]),
    help="Enter service name. Options : queue or store",
    required=True,
)
def reset(service):
    print("reset", service)
    if service == "store":
        Store = store.get_store(
            StoreConfig(
                label="store",
                type="es_vec",
                parameters=StoreParameters(
                    host_name="es",
                    image_index_name="image",
                    video_index_name="video",
                    text_index_name="text",
                ),
            )
        )
        Store.connect()
        Store.reset()
        print("Store reset")
    elif service == "queue":
        queue = Queue.make(
            QueueConfig(
                label="Queue",
                type="rabbitmq",
                parameters=QueueParameters(
                    host_name="rabbitmq",
                    queues=[
                        {"name": "tattle-search-index-queue"},
                        {"name": "tattle-search-report-queue"},
                    ],
                ),
            )
        )
        queue.connect()
        queue.reset()

@cli.command()
@click.option(
    "-s",
    "--service",
    type=click.Choice(["queue", "store"]),
    help="Enter service name. Options : queue or store",
    required=True,
)
def seed(service):
    print("seed", service)
    if service == "store":
        Store = store.get_store(
            StoreConfig(
                label="store",
                type="es_vec",
                parameters=StoreParameters(
                    host_name="es",
                    image_index_name="image",
                    video_index_name="video",
                    text_index_name="text",
                ),
            )
        )
        Store.connect()
        Store.optionally_create_index()
        print("Store reset")
    elif service == "queue":
        queue = Queue.make(
            QueueConfig(
                label="Queue",
                type="rabbitmq",
                parameters=QueueParameters(
                    host_name="rabbitmq",
                    queues=[
                        {"name": "tattle-search-index-queue"},
                        {"name": "tattle-search-report-queue"},
                    ],
                ),
            )
        )
        queue.connect()
        queue.initialize()

@cli.command()
@click.option(
    "-s",
    "--service",
    type=click.Choice(["queue", "store"]),
    help="Enter service name. Options : queue or store",
    required=True,
)
def stats(service):
    print("stats", service)
    if service == "store":
        Store = store.get_store(
            StoreConfig(
                label="store",
                type="es_vec",
                parameters=StoreParameters(
                    host_name="es",
                    image_index_name="image",
                    video_index_name="video",
                    text_index_name="text",
                ),
            )
        )
        Store.connect()
        stats = Store.stats()
        logger.prettyprint(stats)
    elif service == "queue":
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
        rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
        rabbitmq_username = os.getenv('RABBITMQ_USERNAME', 'guest')
        rabbitmq_password = os.getenv('RABBITMQ_PASSWORD', 'guest')

        credentials = pika.PlainCredentials(rabbitmq_username, rabbitmq_password)
        parameters = pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        queue_names = ["tattle-search-index-queue", "tattle-search-report-queue"]
        total_messages = 0

        for queue_name in queue_names:
            queue_stats = channel.queue_declare(queue=queue_name, passive=True)
            total_messages += queue_stats.method.message_count

        click.echo(f"Total messages in queues: {total_messages}")

        connection.close()

if __name__ == "__main__":
    cli()

   
