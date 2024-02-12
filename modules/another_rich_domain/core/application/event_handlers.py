from modules.another_rich_domain.core.domain.events import SomeResourceCreated

from building_blocks.application.event_handlers import DomainEventHandler


class UpdateThisResource(DomainEventHandler[SomeResourceCreated]):
    async def handle(self, event: SomeResourceCreated) -> None:
        print(f"Updating resource {event.id} in another rich domain")  # noqa: T201
