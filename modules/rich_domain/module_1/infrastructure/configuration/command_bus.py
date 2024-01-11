import injector

from modules.rich_domain.module_1.core.application.commands.rich_domain_model import (
    CreateRichDomainModel,
    CreateRichDomainModelHandler,
)

from building_blocks.within_bounded_context.application.command_bus import CommandToHandlerMapping


@injector.inject
def configure_commands_mapping(commands_mapping: CommandToHandlerMapping, container: injector.Injector) -> None:
    for command, handler_cls in [
        (CreateRichDomainModel, CreateRichDomainModelHandler),
    ]:
        commands_mapping[command] = handler_cls
        container.binder.bind(handler_cls, to=handler_cls)
