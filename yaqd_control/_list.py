__all__ = ["list"]


import json
import toml

import prettytable  # type: ignore

from ._cache import read_daemon_cache


def list(format="prettytable"):
    dd = {}
    for daemon in read_daemon_cache():
        dd[f"{daemon.host}:{daemon.port}"] = daemon.__dict__
    if format == "json":
        return json.dumps(dd)
    elif format == "toml":
        return toml.dumps(dd)
    elif format == "prettytable":
        out = prettytable.PrettyTable()
        out.field_names = ["host", "port", "kind", "name"]
        out.align = "l"
        for daemon in dd.values():
            out.add_row([daemon["host"], daemon["port"], daemon["kind"], daemon["name"]])
        return out
    else:
        raise KeyError(f"format {format} not recognized in yaqd list")
