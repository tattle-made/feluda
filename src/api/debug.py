#!/usr/bin/env python

import click
from core.config import StoreConfig, StoreParameters
from core import store


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
                    host_name="es",
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
        pass


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
        pass


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


if __name__ == "__main__":
    cli()
