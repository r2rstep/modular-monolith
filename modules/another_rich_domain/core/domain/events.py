from building_blocks.domain.event import DomainEvent
from modules.another_rich_domain.language import SomeModelId


class SomeResourceCreated(DomainEvent):
    id: SomeModelId  # noqa: A003
