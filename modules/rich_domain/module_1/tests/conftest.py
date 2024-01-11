import pytest

from infrastructure.event_bus import EventBus


@pytest.fixture()
def event_bus() -> EventBus:
    return EventBus()


@pytest.fixture(autouse=True)
def _module_startup() -> None:
    from modules.rich_domain.module_1.infrastructure.startup import startup as module_1_startup
    from modules.rich_domain.module_2.infrastructure.startup import startup as module_2_startup

    module_1_startup()
    module_2_startup()
