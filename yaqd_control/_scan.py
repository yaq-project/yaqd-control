__all__ = ["scan"]


import json
import socket
from pprint import pprint
from dataclasses import fields
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
        # probe socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, i))
            s.sendall(b'{"jsonrpc":"2.0", "method": "id", "id":"find"}')
            ident = json.loads(s.recv(1024))
            kind = ident["result"]["kind"]
            name = ident["result"]["name"]
            s.sendall(b'{"jsonrpc":"2.0", "method": "config_filepath", "id":"find"}')
            config_filepath = json.loads(s.recv(1024))["result"]
        except Exception as e:
            if i in old_ports.keys():
                kind = old_ports[i].kind
                name = old_ports[i].name
                print(f"...known daemon {kind}:{name} on port {i} not responding")
            continue
        # format result
        kwargs = {k: v for k, v in ident["result"].items() if k in DaemonData.get_field_names()}
        kwargs["host"] = host
        kwargs["port"] = i
        kwargs["config_filepath"] = config_filepath
        dd = DaemonData(**kwargs)
        # give feedback
        if i not in old_ports.keys():
            print(f"...found new daemon {kind}:{name} on port {i}")
        elif old_ports[i] != dd:
            print(f"...updated daemon {kind}:{name} attributes on port {i}")
        else:
            print(f"...saw unchanged daemon {kind}:{name} on port {i}")
        # finish
        write_to_daemon_cache(dd)
        s.close()
    print("...done!")
