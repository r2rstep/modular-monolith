from commons.messagebox.infrastructure.messagebox import Inbox
from modules.rich_domain.module_2.infrastructure import settings


def init_inbox() -> Inbox:
    return Inbox(settings.MODULE_NAME)
