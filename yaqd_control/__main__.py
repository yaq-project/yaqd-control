#!/usr/bin/env python3

import os
import pathlib
import subprocess
import sys

import appdirs  # type: ignore
import click

from .__version__ import __version__
from ._cache import add_config, clear_cache, read_daemon_cache
from ._enablement import enable, disable, start, stop, reload, restart
from ._scan import scan
from ._status import status
from ._list import list as list_


@click.group()
@click.version_option(__version__)
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
            if sys.platform.startswith("win32"):
                config_filepath = str(config_filepath)
                subprocess.run([os.environ.get("EDITOR", "notepad.exe"), config_filepath])
            else:
                subprocess.run([os.environ.get("EDITOR", "vi"), config_filepath])
            try:
                add_config(config_filepath)
                break
            except Exception:

                if not click.confirm(
                    "Error updating cache. Would you like to re-edit the config?",
                    default=True,
                ):
                    break


@main.command(name="status")
def _status():
    status()


@main.command(name="list")
def _list():
    list_()


def _parse_kinds(daemon, all_):
    known_daemons = read_daemon_cache()
    known_kinds = set(d.kind for d in known_daemons)
    if all_:
        daemon = known_kinds
    return daemon


all_option = click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    default=False,
    help="Apply to all known daemons.",
)


@main.command(name="enable")
@click.argument("daemon", nargs=-1)
@all_option
@click.option(
    "--password",
    "-p",
    prompt=sys.platform.startswith("win32"),
    hide_input=True,
    help="Password for user account, only used on Windows",
)
def _enable(daemon, all_=False, password=None):
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        if d.endswith(".toml"):
            d = pathlib.Path(d).absolute()
            add_config(d)
            known_daemons = read_daemon_cache()
            d = next(
                dd.kind
                for dd in known_daemons
                if pathlib.Path(dd.config_filepath).absolute() == d
            )
        enable(d, password)


@main.command(name="disable")
@click.argument("daemon", nargs=-1)
@all_option
def _disable(daemon, all_=False):
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        disable(d)


@main.command(name="start")
@click.argument("daemon", nargs=-1)
@all_option
def _start(daemon, all_=False):
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        start(d)


@main.command(name="stop")
@click.argument("daemon", nargs=-1)
@all_option
def _stop(daemon, all_=False):
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        stop(d)


@main.command(name="restart")
@click.argument("daemon", nargs=-1)
@all_option
def _restart(daemon, all_=False):
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        restart(d)


@main.command(name="reload")
@click.argument("daemon", nargs=-1)
@all_option
def _reload(daemon, all_=False):
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        reload(d)


if __name__ == "__main__":
    main()
