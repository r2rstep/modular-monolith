import pytest

from app.application import process_inboxes
from commons.messagebox.application.process_messagebox import ProcessInbox
from modules.rich_domain import module_1
from tests.test_app.conftest import api_client, app  # noqa: F401


@pytest.fixture(autouse=True)
def _override_process_inboxes(app):  # noqa: F811
    async def overriden_process_inboxes() -> None:
        await module_1.interface.get_module().message_bus.execute(ProcessInbox())

    app.dependency_overrides[process_inboxes] = overriden_process_inboxes
