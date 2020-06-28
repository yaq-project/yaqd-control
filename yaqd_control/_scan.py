__all__ = ["scan"]


import socket
from pprint import pprint
from dataclasses import fields

import yaqc  # type: ignore

from ._daemon_data import DaemonData
from ._cache import read_daemon_cache, write_to_daemon_cache


def scan(host="127.0.0.1", start=36000, stop=39999):
    # gather information about known daemons
    old = read_daemon_cache()
    old_ports = {}
    for dd in old:
        if dd.host == host:
            old_ports[dd.port] = dd
    #
    print(f"scanning host {host} from {start} to {stop}...")
    for i in range(start, stop + 1):
        kwargs = dict()
        try:
            c = yaqc.Client(host=host, port=i)
            kwargs["host"] = host
            kwargs["port"] = i
            kwargs["kind"] = c.id()["kind"]
            kwargs["name"] = c.id()["name"]
            kwargs["config_filepath"] = c.get_config_filepath()
            kwargs["make"] = c.id()["make"]
            kwargs["model"] = c.id()["model"]
            kwargs["serial"] = c.id()["serial"]
        except Exception as e:
            if i in old_ports.keys():
                kind = old_ports[i].kind
                name = old_ports[i].name
                print(f"...known daemon {kind}:{name} on port {i} not responding")
            continue
        # format result
        dd = DaemonData(**kwargs)
        # give feedback
        if i not in old_ports.keys():
            print(f"...found new daemon {dd.kind}:{dd.name} on port {i}")
        elif old_ports[i] != dd:
            print(f"...updated daemon {dd.kind}:{dd.name} attributes on port {i}")
        else:
            print(f"...saw unchanged daemon {dd.kind}:{dd.name} on port {i}")
        # finish
        write_to_daemon_cache(dd)
    print("...done!")
