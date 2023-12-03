from pathlib import Path

import mypy.api


def test_mypy():
    app_path = Path(__file__).parent.parent
    pyproject_path = app_path.parent / "pyproject.toml"
    mypy.api.run(["--config-file", str(pyproject_path), str(app_path)])
