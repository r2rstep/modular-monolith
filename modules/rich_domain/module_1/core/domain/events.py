from modules.rich_domain.module_1.core.domain.models import RichDomainModelName

from building_blocks.types import PK
from building_blocks.within_bounded_context.domain.events import DomainEvent


class RichDomainModelCreated(DomainEvent):
    pk: PK
    name: RichDomainModelName
    is_public: bool = True
