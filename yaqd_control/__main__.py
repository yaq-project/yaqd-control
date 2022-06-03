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


debug_option = click.option(
    "--debug",
    "debug",
    is_flag=True,
    default=False,
)


all_option = click.option(
    "-a",
    "--all",
    "all_",
    is_flag=True,
    default=False,
    help="Apply to all known daemons.",
)


@main.command(name="clear-cache")
@debug_option
def _clear_cache(debug=False):
    if not debug:
        sys.tracebacklimit = 0
    clear_cache()


@main.command(name="scan")
@click.option("--host", default="127.0.0.1", help="Host to scan.")
@click.option("--start", default=36000, help="Scan starting point.")
@click.option("--stop", default=39999, help="Scan stopping point.")
@debug_option
def _scan(host, start, stop, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    scan(host=host, start=start, stop=stop)


@main.command(name="edit-config")
@click.argument("kind", nargs=-1)
@debug_option
def edit_config(kind, debug=False):
    if not debug:
        sys.tracebacklimit = 0
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
                import shutil

                editor = shutil.which(os.environ.get("EDITOR", "notepad.exe"))
                subprocess.run([editor, config_filepath])
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
@click.option(
    "--force-color", "-c", default=False, is_flag=True, type=bool, help="Force color output"
)
@debug_option
def _status(force_color=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    status(force_color)


@main.command(name="list")
@click.option(
    "--format",
    "-f",
    default="prettytable",
    type=click.Choice(["prettytable", "json", "toml", "happi"], case_sensitive=False),
    help="Output format",
)
@debug_option
def _list(format=format, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    out = list_(format=format)
    click.echo(out)


def _parse_name(daemon):
    daemonList = list(daemon)
    for i, d in enumerate(daemon):
        if d.startswith("yaqd-"):
            daemonList[i] = d[5:]
    return tuple(daemonList)


def _parse_kinds(daemon, all_):
    known_daemons = read_daemon_cache()
    known_kinds = set(d.kind for d in known_daemons)
    if all_:
        daemon = known_kinds
    daemon = _parse_name(daemon)
    return daemon


@main.command(name="enable")
@click.argument("daemon", nargs=-1)
@debug_option
@all_option
@click.option(
    "--password",
    "-p",
    prompt=sys.platform.startswith("win32"),
    hide_input=True,
    help="Password for user account, only used on Windows",
)
def _enable(daemon, all_=False, password=None, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        if d.endswith(".toml"):
            d = pathlib.Path(d).absolute()
            add_config(d)
            known_daemons = read_daemon_cache()
            d = next(
                dd.kind for dd in known_daemons if pathlib.Path(dd.config_filepath).absolute() == d
            )
        enable(d, password)


@main.command(name="disable")
@click.argument("daemon", nargs=-1)
@debug_option
@all_option
def _disable(daemon, all_=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        disable(d)


@main.command(name="start")
@click.argument("daemon", nargs=-1)
@debug_option
@all_option
def _start(daemon, all_=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        start(d)


@main.command(name="stop")
@click.argument("daemon", nargs=-1)
@debug_option
@all_option
def _stop(daemon, all_=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        stop(d)


@main.command(name="restart")
@click.argument("daemon", nargs=-1)
@debug_option
@all_option
def _restart(daemon, all_=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        restart(d)


@main.command(name="reload")
@click.argument("daemon", nargs=-1)
@debug_option
@all_option
def _reload(daemon, all_=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0
    daemon = _parse_kinds(daemon, all_)
    for d in daemon:
        reload(d)


@main.command(name="nssm")
@click.argument("args", nargs=-1)
@debug_option
def _nssm(args, debug=False):
    """Windows-only pass-through for bundled NSSM."""
    if not debug:
        sys.tracebacklimit = 0
    here = pathlib.Path(__file__).parent
    path = here / "bin" / "nssm.exe"
    args = list(args)
    args.insert(0, path)
    subprocess.Popen(args)


if __name__ == "__main__":
    main()
