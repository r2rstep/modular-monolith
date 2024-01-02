import pytest

from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus


@pytest.fixture()
def event_bus() -> EventBus:
    return EventBus()


@pytest.fixture(autouse=True)
def _module_startup() -> None:
    from modules.rich_domain.module_1.infrastructure.startup import startup

    startup()
