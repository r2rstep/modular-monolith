import pytest
from starlette.testclient import TestClient

from app.application import app as fastapi_app


@pytest.fixture()
def app():
    return fastapi_app


@pytest.fixture()
def api_client(app):
    return TestClient(app)
