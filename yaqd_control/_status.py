__all__ = ["status"]

from functools import partial
from multiprocessing import Pool

from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich.console import Console

import yaqc  # type: ignore

from ._cache import read_daemon_cache


def connect(daemon):
    c = yaqc.Client(host=daemon.host, port=daemon.port)
    busy = c.busy()
    name = c.id()["name"]
    return busy, name


def fill(busy, name, online_text, busy_text, name_text):
    online_text.append("online", style="green")
    busy_text.append(str(busy), style="red" if busy else "green")
    name_text.append(name)


def fill_error(e, online_text, busy_text, name_text, name_fallback):
    online_text.append("offline", style="red")
    busy_text.append("?", style="red")
    name_text.append(name_fallback)


def status(force_color=False):
    pool = Pool()
    table = Table()
    for field in ["host", "port", "kind", "name", "status", "busy"]:
        table.add_column(field)

    if force_color:
        console = Console(force_terminal=force_color)
    else:
        console = None
    with Live(table, refresh_per_second=4, console=console) as live:
        results = []
        for daemon in read_daemon_cache():
            online_text = Text("")
            busy_text = Text("")
            name_text = Text("")
            table.add_row(
                daemon.host,
                str(daemon.port),
                daemon.kind,
                name_text,
                online_text,
                busy_text,
            )
            results.append(
                pool.apply_async(
                    connect,
                    (daemon,),
                    callback=partial(fill, online_text=online_text, busy_text=busy_text, name_text=name_text),
                    error_callback=partial(
                        fill_error, online_text=online_text, busy_text=busy_text, name_text=name_text, name_fallback=daemon.name
                    ),
                )
            )

        # Wait for all the results before exiting live view
        for r in results:
            r.wait()
