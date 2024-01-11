from commons.messagebox.infrastructure.messagebox import Outbox
from modules.rich_domain.module_2.infrastructure import settings


def init_outbox() -> Outbox:
    return Outbox(settings.MODULE_NAME)
