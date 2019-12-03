__all__ = ["list"]


from ._cache import read_daemon_cache
import prettytable  # type: ignore


def list():
    out = prettytable.PrettyTable()
    out.field_names = ["host", "port", "kind", "name"]
    out.align = "l"
    for daemon in read_daemon_cache():
        out.add_row([daemon.host, daemon.port, daemon.kind, daemon.name])
    print(out)
