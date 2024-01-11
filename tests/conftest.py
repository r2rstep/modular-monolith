from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def pyproject_toml_path() -> Path:
    return Path(__file__).parent.parent / "pyproject.toml"
