import argparse
import pathlib
import subprocess
import sys

import appdirs
import toml

def main():
    parser = argparse.ArgumentParser(description="Start yaq daemons with configs in a folder")

    parser.add_argument("config_dir", nargs="?", default=appdirs.user_config_dir("yaqd", "yaq"))

    args = parser.parse_args()
    config = pathlib.Path(args.config_dir)

    tomls = config.rglob("*.toml")
    if len(tomls) == 0:
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
            proc = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(f"PID: {proc.pid} - {" ".join(cmd)}")
    
if __name__ == "__main__":
    main()
