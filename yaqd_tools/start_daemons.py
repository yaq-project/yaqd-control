import argparse
import pathlib
import subprocess

import appdirs
import toml

def main():
    parser = argparse.ArgumentParser(description="Start yaq daemons with configs in a folder")

    parser.add_argument("config_dir", nargs="?", default=appdirs.user_config_dir("yaqd", "yaq"))

    args = parser.parse_args()
    config = pathlib.Path(args.config_dir)

    for fp in config.rglob("*.toml"):
        if fp.stem.endswith("state"):
            continue
        with open(fp, "r") as f: 
            try:
                cd = toml.load(f)
            except toml.TomlDecodeError as e:
                print(e)
                print(fp)
                continue
            if not cd.get("enable", True):
                continue
            if "entry" not in cd:
                continue

            proc = subprocess.Popen([cd["entry"], "--config", str(fp)], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(f"PID: {proc.pid}: {cd['entry']} --config {fp}")
    
if __name__ == "__main__":
    main()
