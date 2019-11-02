__all__ = ["read_daemon_cache", "write_daemon_cache"]


import pathlib
import appdirs
import toml
from ._daemon_data import DaemonData


daemeon_cache_path = (
    pathlib.Path(appdirs.user_cache_dir(appname="yaqd-control", appauthor="yaq"))
    / "daemon-cache.toml"
)

daemeon_cache_path.parent.mkdir(parents=True, exist_ok=True)


# TODO: consider adding lockfile for cache


def clear_cache():
    try:
        daemeon_cache_path.unlink()
    except FileNotFoundError:
        print("cache already clear!")


def read_daemon_cache():
    # read
    try:
        with open(daemeon_cache_path, "r") as f:
            dic = toml.load(f)
    except FileNotFoundError:
        dic = {}
    # process
    out = []
    for v in dic.values():
        dd = DaemonData(**v)
        out.append(dd)
    # return
    return out


def write_to_daemon_cache(daemon_data):
    # read
    try:
        with open(daemeon_cache_path, "r") as f:
            dic = toml.load(f)
    except FileNotFoundError:
        dic = {}
    # extend
    dic[f"{daemon_data.host}:{daemon_data.port}"] = daemon_data.as_dict()
    # write
    with open(daemeon_cache_path, "wt") as f:
        toml.dump(dic, f)
