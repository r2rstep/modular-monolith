from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def pyproject_toml_path() -> Path:
    return Path(__file__).parent.parent / "pyproject.toml"


@pytest.fixture(scope="session")
def existing_modules() -> list[str]:
    modules = list(Path(__file__).parent.parent.glob("modules/**/core"))
    modules = [str(module)[str(module).find("/modules/") :] for module in modules]
    return [module.lstrip("/").rstrip("/core").replace("/", ".") for module in modules]
