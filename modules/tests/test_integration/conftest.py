import pytest

from app.infrastructure.startup import start_modules


@pytest.fixture(autouse=True)
def _startup() -> None:
    start_modules()
