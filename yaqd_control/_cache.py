__all__ = ["read_daemon_cache", "write_daemon_cache"]


import pathlib
import appdirs  # type: ignore
import toml
from ._daemon_data import DaemonData


daemon_cache_path = (
    pathlib.Path(appdirs.user_cache_dir(appname="yaqd-control", appauthor="yaq"))
    / "daemon-cache.toml"
)

daemon_cache_path.parent.mkdir(parents=True, exist_ok=True)


# TODO: consider adding lockfile for cache


def clear_cache():
    try:
        daemon_cache_path.unlink()
    except FileNotFoundError:
        print("cache already clear!")


def read_daemon_cache():
    # read
    try:
        with open(daemon_cache_path, "r") as f:
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
        with open(daemon_cache_path, "r") as f:
            dic = toml.load(f)
    except FileNotFoundError:
        dic = {}
    # extend
    dic[f"{daemon_data.host}:{daemon_data.port}"] = daemon_data.as_dict()
    # write
    with open(daemon_cache_path, "wt") as f:
        toml.dump(dic, f)


def add_config(filepath):
    filepath = pathlib.Path(filepath).absolute()
    with open(filepath, "r") as f:
        dic = toml.load(f)
    kind = filepath.parent.name
    if kind.startswith("yaqd-"):
        kind = kind[5:]
    for k, v in dic.items():
        if k in ("enable", "shared-settings"):
            continue
        dd = DaemonData(
            kind=kind,
            host="127.0.0.1",
            port=v["port"],
            name=k,
            config_filepath=str(filepath),
        )
        write_to_daemon_cache(dd)
