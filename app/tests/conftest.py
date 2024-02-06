import pytest

from app.infrastructure.startup import start_modules
from tests.test_app.conftest import api_client, app  # noqa: F401


@pytest.fixture(autouse=True)
def _startup() -> None:
    start_modules()
