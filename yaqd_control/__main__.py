#!/usr/bin/env python3


import click
from ._cache import clear_cache
from ._scan import scan
from ._start import start
from ._status import status
from ._list import list as list_


@click.group()
def main():
    pass


@main.command(name="clear-cache")
def _clear_cache():
    clear_cache()


@main.command(name="scan")
@click.option("--host", default="127.0.0.1", help="Host to scan.")
@click.option("--start", default=36000, help="Scan starting point.")
@click.option("--stop", default=39999, help="Scan stopping point.")
def _scan(host, start, stop):
    scan(host=host, start=start, stop=stop)


@main.command(name="start")
@click.argument("directory", required=False, type=click.Path())
def _start(directory):
    start(directory)


@main.command(name="status")
def _status():
    status()


@main.command(name="list")
def _list():
    list_()


if __name__ == "__main__":
    main()
