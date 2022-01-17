#!/usr/bin/env python

import click
from core.config import QueueConfig, QueueParameters, StoreConfig, StoreParameters
from core import store
from core.logger import Logger
from core.queue import Queue

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
        print("function not implemented")
        pass


if __name__ == "__main__":
    cli()
