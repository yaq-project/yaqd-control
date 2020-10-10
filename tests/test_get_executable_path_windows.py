# this script uses the fake_process pytest figure
# which is provided by the pytest-subprocess package


import pytest

from yaqd_control._enablement import _get_executable_path_windows


def test_single_exe(fake_process):
    exe = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes.exe"
    fake_process.register_subprocess(["where", "yaqd-fakes"], stdout=exe)
    out = _get_executable_path_windows("fakes")
    assert out == exe


def test_single_cmd(fake_process):
    cmd = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes.cmd"
    fake_process.register_subprocess(["where", "yaqd-fakes"], stdout=cmd)
    out = _get_executable_path_windows("fakes")
    assert out == cmd


def test_empty(fake_process):
    fake_process.register_subprocess(["where", "yaqd-fakes"], stdout="")
    with pytest.raises(FileNotFoundError):
        out = _get_executable_path_windows("fakes")


def test_bad(fake_process):
    bad = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes"
    fake_process.register_subprocess(["where", "yaqd-fakes"], stdout=bad)
    with pytest.raises(FileNotFoundError):
        out = _get_executable_path_windows("fakes")


def test_cmd_exe(fake_process):
    exe = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes.exe"
    cmd = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes.cmd"
    out = cmd + "\n" + exe
    fake_process.register_subprocess(["where", "yaqd-fakes"], stdout=out)
    out = _get_executable_path_windows("fakes")
    assert out == exe


def test_exe_cmd(fake_process):
    exe = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes.exe"
    cmd = "C:\\Users\\Blaise\\Miniconda3\\Scripts\\yaqd-fakes.cmd"
    out = exe + "\n" + cmd
    fake_process.register_subprocess(["where", "yaqd-fakes"], stdout=out)
    out = _get_executable_path_windows("fakes")
    assert out == exe
