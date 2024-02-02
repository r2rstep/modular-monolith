import pytest

from commons.event_bus.application.event_bus import EventBus


@pytest.fixture()
def event_bus() -> EventBus:
    return EventBus()


@pytest.fixture(autouse=True)
def _module_startup() -> None:
    from modules.rich_domain.module_2.infrastructure.startup import startup

    startup()
