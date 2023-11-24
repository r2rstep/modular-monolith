from pathlib import Path
import subprocess
import sysconfig


def test_ruff():
    ruff = Path(sysconfig.get_path("scripts")) / "ruff"

    print("\n")  # noqa: T201
    assert subprocess.run([ruff, "check", ".."]).returncode == 0  # noqa: PLW1510
    assert subprocess.run([ruff, "format", "--check", ".."]).returncode == 0  # noqa: PLW1510
