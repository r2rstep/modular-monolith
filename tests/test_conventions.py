from pathlib import Path
import subprocess
import sysconfig


def test_ruff():
    ruff = Path(sysconfig.get_path("scripts")) / "ruff"

    print("\n")  # noqa: T201
    stdout, stderr, exit_code = _run([ruff, "check", "."])
    assert exit_code == 0, f"ruff check failed: {stdout}"
    stdout, stderr, exit_code = _run([ruff, "format", "--check", "."])
    assert exit_code == 0, f"ruff format check failed: {stdout}"


def _run(cmd: list[str]) -> tuple[str, str, int]:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    return out.decode("utf-8"), err.decode("utf-8"), errcode
