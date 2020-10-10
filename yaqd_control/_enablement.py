__all__ = ["enable", "disable", "start", "stop", "restart", "reload"]

import getpass
import pathlib
import subprocess
import sys
import tempfile

import appdirs  # type: ignore

from ._cache import add_config, read_daemon_cache
from enum import Enum

# Linux
service_template = """
[Unit]
Description=yaqd-{kind}

[Service]
Type=simple
User={user}
ExecStart={executable} --config={config_path}
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
"""

# MacOS
plist_file = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.yaqd-{kind}.daemon</string>

        <key>UserName</key>
        <string>{user}</string>

        <key>ProgramArguments</key>
        <array>
          <string>{executable}</string>
          <string>--config={config_path}</string>
        </array>
    </dict>
</plist>
"""

# Other templates
plist_full_path_template = "/Library/LaunchDaemons/com.yaqd-{kind}.daemon.plist"
daemon_label = "com.yaqd-{kind}.daemon"
yaq_kind_template = "yaqd-{kind}"

# Windows specific exe, empty string for other Operating Systems
nssm_exe = ""


class Action(str, Enum):
    disable: str = "disable"
    enable: str = "enable"
    install: str = "install"
    load: str = "load"
    reload: str = "reload"
    remove: str = "remove"
    restart: str = "restart"
    set: str = "set"
    start: str = "start"
    stop: str = "stop"
    unload: str = "unload"


if sys.platform.startswith("win32"):
    try:
        nssm_exe = (
            subprocess.run(["where", "nssm.exe"], capture_output=True, check=True)
            .stdout.decode()
            .strip()
            .split("\n")[0]
        )
    except Exception:
        nssm_exe = str(pathlib.Path(__file__).parent / "bin" / "nssm.exe")


def enable(kind, password=None):
    if sys.platform.startswith("win32"):
        _enable_for_windows(kind, password)
    elif sys.platform.startswith("linux"):
        _enable_for_linux(kind)
    elif sys.platform.startswith("darwin"):
        _enable_for_macOS(kind)
    else:
        raise NotImplementedError


def disable(kind):
    if sys.platform.startswith("win32"):
        _run_nssm_exe_by_action(Action.remove, kind)
    elif sys.platform.startswith("linux"):
        _run_systemctl_command_by_action(Action.disable, kind)
    elif sys.platform.startswith("darwin"):
        _run_launchctl_command_by_action(Action.unload, kind)
    else:
        raise NotImplementedError


def start(kind):
    if sys.platform.startswith("win32"):
        _run_nssm_exe_by_action(Action.start, kind)
    elif sys.platform.startswith("linux"):
        _run_systemctl_command_by_action(Action.start, kind)
    elif sys.platform.startswith("darwin"):
        _run_launchctl_command_by_action(Action.start, kind)
    else:
        raise NotImplementedError


def stop(kind):
    if sys.platform.startswith("win32"):
        _run_nssm_exe_by_action(Action.stop, kind)
    elif sys.platform.startswith("linux"):
        _run_systemctl_command_by_action(Action.stop, kind)
    elif sys.platform.startswith("darwin"):
        _run_launchctl_command_by_action(Action.stop, kind)
    else:
        raise NotImplementedError


def restart(kind):
    if sys.platform.startswith("win32"):
        _run_nssm_exe_by_action(Action.restart, kind)
    elif sys.platform.startswith("linux"):
        _run_systemctl_command_by_action(Action.restart, kind)
    elif sys.platform.startswith("darwin"):
        _run_launchctl_command_by_action(Action.restart, kind)
    else:
        raise NotImplementedError


def reload(kind):
    if sys.platform.startswith("win32"):
        _run_nssm_exe_by_action(Action.restart, kind)
    elif sys.platform.startswith("linux"):
        _run_systemctl_command_by_action(Action.reload, kind)
    elif sys.platform.startswith("darwin"):
        _run_launchctl_command_by_action(Action.restart, kind)
    else:
        raise NotImplementedError


def _format_config_template(template: str, kind: str):
    return template.format(
        kind=kind,
        executable=_get_executable_path(kind),
        config_path=_get_config_path(kind),
        user=getpass.getuser(),
    ).encode()


def _get_executable_path(kind: str):
    return (
        subprocess.run(["which", f"yaqd-{kind}"], capture_output=True, check=True)
        .stdout.decode()
        .strip()
    )


def _get_executable_path_windows(kind: str):
    where = (
        subprocess.run(["where", f"yaqd-{kind}"], capture_output=True, check=True)
        .stdout.decode()
        .strip()
    )
    for desired in [".exe", ".cmd"]:
        for pth in where.split("\n"):
            if pth.endswith(desired):
                return pth
    raise FileNotFoundError(f"Could not find executable {kind}")


def _enable_for_windows(kind: str, password: str):
    if password is None:
        raise ValueError("Windows services require a password")
    executable = _get_executable_path_windows(kind)
    _run_nssm_exe_by_action(
        Action.install, kind, True, executable, f"--config={_get_config_path(kind)}"
    )
    _run_nssm_exe_by_action(
        Action.set, kind, True, "ObjectName", f".\\{getpass.getuser()}", password
    )


def _enable_for_linux(kind: str):
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(_format_config_template(service_template, kind))
        tf.flush()
        service_template_full_path = f"/etc/systemd/system/yaqd-{kind}.service"
        subprocess.run(
            ["sudo", "cp", tf.name, service_template_full_path],
            check=True,
        )
        subprocess.run(
            ["sudo", "chmod", "+r", service_template_full_path],
            check=True,
        )
    _run_systemctl_command_by_action(Action.enable, kind)


def _enable_for_macOS(kind: str):
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(_format_config_template(plist_file, kind))
        tf.flush()
        subprocess.run(
            ["sudo", "cp", tf.name, plist_full_path_template.format(kind=kind)],
            check=True,
        )
    _run_launchctl_command_by_action(Action.load, kind)


def _get_config_path(kind: str):
    known_daemons = read_daemon_cache()
    try:
        daemon_data = next(d for d in known_daemons if d.kind == kind)
        config_path = daemon_data.config_filepath
    except:
        config_path = pathlib.Path(appdirs.user_config_dir("yaqd", "yaq")) / kind / "config.toml"
        add_config(config_path)
    return config_path


def _run_nssm_exe_by_action(action: Action, kind: str, check: bool = False, *additional_args):
    command = [nssm_exe, action, yaq_kind_template.format(kind=kind)]
    for arg in additional_args:
        command.append(arg)
    subprocess.run(command, check=check)


def _run_systemctl_command_by_action(action: Action, kind: str):
    subprocess.run(["systemctl", action, yaq_kind_template.format(kind=kind)])


def _run_launchctl_command_by_action(action: Action, kind: str):
    if action == "load" or action == "unload":
        subprocess.run(["launchctl", action, plist_full_path_template.format(kind=kind)])
    else:
        subprocess.run(["launchctl", action, daemon_label.format(kind=kind)])
