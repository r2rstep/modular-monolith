import pytest

from modules.crud.core.application.commands.messagebox import ProcessInbox

from app.application import process_inboxes
from modules import crud
from tests.test_app.conftest import api_client, app  # noqa: F401


@pytest.fixture(autouse=True)
def _override_process_inboxes(app):  # noqa: F811
    async def overriden_process_inboxes() -> None:
        await crud.interface.get_module().message_bus.execute(ProcessInbox())

    app.dependency_overrides[process_inboxes] = overriden_process_inboxes
