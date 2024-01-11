from modules.rich_domain.module_1.core.domain.models import RichDomainModelName

from building_blocks.within_bounded_context.application.command import Command


class DoSomething(Command):
    name: RichDomainModelName
