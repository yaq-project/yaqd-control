import argparse
import pathlib
import subprocess
import sys

import appdirs
import toml


def start(config_dir=None):
    if config_dir is None:
        config_dir = appdirs.user_config_dir("yaqd", "yaq")
    config = pathlib.Path(config_dir)
    tomls = config.rglob("*.toml")
    if not tomls:
        print(f"No config files found in {config}")
    for fp in config.rglob("*.toml"):
        if fp.stem.endswith("state"):
            continue
        with open(fp, "r") as f:
            try:
                cd = toml.load(f)
            except toml.TomlDecodeError as e:
                print(e, file=sys.stderr)
                print(fp, file=sys.stderr)
                continue
            if not cd.get("enable", True):
                continue
            if "entry" not in cd:
                continue

            cmd = [cd["entry"], "--config", str(fp)]
            print(fp)
            proc = subprocess.Popen(
                cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL
            )
            print(f"PID: {proc.pid} - {' '.join(cmd)}")
