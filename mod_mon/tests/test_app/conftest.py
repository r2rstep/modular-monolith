import pytest
from starlette.testclient import TestClient

from mod_mon.api.application import app


@pytest.fixture()
def api_client():
    return TestClient(app)
