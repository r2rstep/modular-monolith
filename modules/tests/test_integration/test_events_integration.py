import pytest

from modules.another_rich_domain.core.domain.events import SomeResourceCreated
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated
from modules.rich_domain.module_2.core.application.module_1_events_handlers import DoSomething

from commons.container.infrastructure.global_container import get_global_container
from commons.database.db import InMemoryDb
from modules.another_rich_domain.interface import get_module as get_another_rich_domain_module
from modules.another_rich_domain.language import SomeModelId
from modules.rich_domain.language import RichDomainModelName
from modules.rich_domain.module_1.interface import get_module as get_module_1
from modules.rich_domain.module_2.interface import get_module as get_module_2
from tests.helpers import excluding_occurred_at


@pytest.fixture()
def module_1():
    return get_module_1()


@pytest.fixture()
def module_2():
    return get_module_2()


@pytest.fixture()
def another_module():
    return get_another_rich_domain_module()


@pytest.fixture()
def db():
    return get_global_container().get(InMemoryDb)


@pytest.fixture()
def process_inboxes(module_1, module_2, another_module):
    async def process():
        await module_1.message_bus.execute(module_1.ProcessInbox())
        await module_2.message_bus.execute(module_2.ProcessInbox())
        await another_module.message_bus.execute(another_module.ProcessInbox())

    return process


@pytest.mark.asyncio()
async def test_integration(module_1, db, process_inboxes):
    created_pk = await module_1.CreateRichDomainModel(name="integration test").handle()

    for _ in range(2):
        await process_inboxes()

    assert excluding_occurred_at(db.get(created_pk)) == excluding_occurred_at(
        RichDomainModelCreated(pk=created_pk, name=RichDomainModelName("integration test"))
    )
    assert db.get("command integration test") == DoSomething(name=RichDomainModelName("integration test"))
    assert excluding_occurred_at(db.get("another integration test")) == excluding_occurred_at(
        SomeResourceCreated(id=SomeModelId("integration test"))
    )
