from commons.messagebox.infrastructure.messagebox import Outbox
from modules.another_rich_domain.infrastructure import settings


def init_outbox() -> Outbox:
    return Outbox(settings.MODULE_NAME)
