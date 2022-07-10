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
    return busy


def fill(busy, online_text, busy_text):
    online_text.append("online", style="green")
    busy_text.append(str(busy), style="red" if busy else "green")


def fill_error(e, online_text, busy_text):
    online_text.append("offline", style="red")
    busy_text.append("?", style="red")


def status(force_color=False, as_list=False):
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
            table.add_row(
                daemon.host,
                str(daemon.port),
                daemon.kind,
                daemon.name,
                online_text,
                busy_text,
            )
            results.append(
                pool.apply_async(
                    connect,
                    (daemon,),
                    callback=partial(fill, online_text=online_text, busy_text=busy_text),
                    error_callback=partial(
                        fill_error, online_text=online_text, busy_text=busy_text
                    ),
                )
            )

        # Wait for all the results before exiting live view
        for r in results:
            r.wait()
    if as_list:
        list_ = list()
        col_length = len(table.columns)
        row_length = table.row_count
        for i in range(col_length):
            col = table.columns[i]._cells
            list_.append(col)
        tuple_ = list(zip(*list_))

        out = list()
        for i in range(len(tuple_)):
            temp = tuple_[i]
            temp2 = list()
            for k in range(len(temp)):
                if k == 4:
                    temp2.append(str(temp[k]))
                elif k == 5:
                    temp2.append(str(temp[k]))
                else:
                    temp2.append(temp[k])
            out.append(temp2)
        return out
    return
