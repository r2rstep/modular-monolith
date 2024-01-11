from building_blocks.within_bounded_context.domain.events import DomainEvent
from commons.types import PK
from modules.rich_domain.language import RichDomainModelName


class RichDomainModelCreated(DomainEvent):
    pk: PK
    name: RichDomainModelName
    is_public: bool = True
