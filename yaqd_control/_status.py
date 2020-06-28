__all__ = ["status"]


import socket
import prettytable  # type: ignore
import colorama  # type: ignore
from colorama import Fore

import yaqc  # type: ignore

from ._cache import read_daemon_cache


def colorify(string, text, color):
    colorama.init()  # for windows
    return string.replace(text, color + text + Fore.RESET)


def status():
    out = prettytable.PrettyTable()
    out.field_names = ["host", "port", "kind", "name", "status", "busy"]
    out.align = "l"
    for daemon in read_daemon_cache():
        try:
            c = yaqc.Client(host=daemon.host, port=daemon.port)
            out.add_row(
                [daemon.host, daemon.port, daemon.kind, daemon.name, "online", c.busy(),]
            )
        except Exception as e:
            print(e)
            out.add_row([daemon.host, daemon.port, daemon.kind, daemon.name, "offline", "?"])
    out = out.get_string()
    out = colorify(out, "online", Fore.GREEN)
    out = colorify(out, "offline", Fore.RED)
    out = colorify(out, "False", Fore.GREEN)
    out = colorify(out, "True", Fore.RED)
    print(out)
