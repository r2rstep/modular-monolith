from pathlib import Path

import mypy.api


def test_mypy(pyproject_toml_path):
    app_path = Path(__file__).parent.parent
    mypy.api.run(["--config-file", str(pyproject_toml_path), str(app_path)])
