__all__ = ["list"]


import json
import toml
import time

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
    elif format == "happi":
        out = []
        timestamp = time.ctime()  # generates string, local time
        for daemon in dd.values():
            d = dict()
            d["_id"] = daemon["name"]
            d["active"] = True
            d["args"] = []
            d["creation"] = timestamp
            d["device_class"] = "yaqc_bluesky.Device"
            d["documentation"] = f"yaq:{daemon['kind']} at {daemon['host']}:{daemon['port']}"
            d["host"] = daemon["host"]
            d["kwargs"] = {
                "host": "{{host}}",
                "name": "{{name}}",
                "port": "{{port}}",
            }
            d["last_edit"] = timestamp
            d["name"] = daemon["name"]
            d["port"] = daemon["port"]
            d["type"] = "yaq._happi.YAQItem"
            out.append(d)
        out = json.dumps(out, indent=2)
        return out
    else:
        raise KeyError(f"format {format} not recognized in yaqd list")
