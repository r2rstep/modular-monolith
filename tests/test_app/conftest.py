import pytest
from starlette.testclient import TestClient

from app.application import app


@pytest.fixture()
def api_client():
    return TestClient(app)
