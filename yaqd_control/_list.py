__all__ = [list]


from ._cache import read_daemon_cache


def list():
    print("host           port      kind      name          ")
    print("-------------------------------------------------")
    for daemon in read_daemon_cache():
        out = ""
        out += f"{daemon.host}".ljust(15)
        out += f"{daemon.port}".ljust(10)
        out += f"{daemon.kind}".ljust(10)
        out += f"{daemon.name}".ljust(10)
        print(out)
