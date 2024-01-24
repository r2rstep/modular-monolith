from pathlib import Path

import mypy.api


class MypyError(Exception):
    pass


def test_mypy(pyproject_toml_path):
    app_path = Path(__file__).parent.parent
    stdout, err, exit_status = mypy.api.run(["--config-file", str(pyproject_toml_path), str(app_path)])

    if exit_status:
        raise MypyError("\n" + (err or stdout))
