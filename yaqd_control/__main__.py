#!/usr/bin/env python3


import click
from ._list import list_
from ._start import start


@click.group()
def main():
    pass


@main.command(name="list")
@click.option("--host", default="127.0.0.1", help="Host to scan.")
@click.option("--start", default=36000, help="Scan starting point.")
@click.option("--stop", default=39999, help="Scan stopping point.")
def _list(host, start, stop):
    list_(host=host, start=start, stop=stop)


@main.command(name="start")
@click.argument("directory", required=False, type=click.Path())
def _start(directory):
    start(directory)


if __name__ == "__main__":
    main()
