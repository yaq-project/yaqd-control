#!/usr/bin/env python3

import os
import pathlib
import subprocess

import appdirs
import click
from ._cache import add_config, clear_cache, read_daemon_cache
from ._enablement import enable, disable
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


@main.command(name="edit-config")
@click.argument("kind", nargs=-1)
def edit_config(kind):
    for k in kind:
        try:
            dd = next(d for d in read_daemon_cache() if d.kind == k)
            config_filepath = pathlib.Path(dd.config_filepath)
        except:
            config_filepath = (
                pathlib.Path(appdirs.user_config_dir("yaqd", "yaq")) / k / "config.toml"
            )
        config_filepath.parent.mkdir(parents=True, exist_ok=True)
        while True:
            subprocess.run([os.environ.get("EDITOR", "vi"), config_filepath])
            try:
                add_config(config_filepath)
                break
            except Exception:

                if not click.confirm("Error updating cache. Would you like to re-edit the config?", default=True):
                    break


@main.command(name="status")
def _status():
    status()


@main.command(name="list")
def _list():
    list_()


@main.command(name="enable")
@click.argument("daemon", nargs=-1)
@click.option("-a", "--all", "all_", is_flag=True, default=False, help="Enable all known daemons.")
def _enable(daemon, all_):
    known_daemons = read_daemon_cache()
    known_kinds = set(d.kind for d in known_daemons)
    if all_:
        daemon = known_kinds
    for d in daemon:
        if d.endswith(".toml"):
            d = pathlib.Path(d).absolute()
            add_config(d)
            known_daemons = read_daemon_cache()
            print(d)
            print([pathlib.Path(dd.config_filepath).absolute() for dd in known_daemons])
            d = next(
                dd.kind for dd in known_daemons if pathlib.Path(dd.config_filepath).absolute() == d
            )
        enable(d)


@main.command(name="disable")
@click.argument("daemon", nargs=-1)
@click.option(
    "-a", "--all", "all_", is_flag=True, default=False, help="Disable all known daemons."
)
def _disable(daemon, all_):
    known_daemons = read_daemon_cache()
    known_kinds = set(d.kind for d in known_daemons)
    if all_:
        daemon = known_kinds
    for d in daemon:
        disable(d)


if __name__ == "__main__":
    main()
