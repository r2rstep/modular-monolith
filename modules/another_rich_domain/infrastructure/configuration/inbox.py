from commons.messagebox.infrastructure.messagebox import Inbox
from modules.another_rich_domain.infrastructure import settings


def init_inbox() -> Inbox:
    return Inbox(settings.MODULE_NAME)
