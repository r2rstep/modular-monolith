from commons.messagebox.infrastructure.messagebox import Inbox
from modules.crud.infrastructure import settings


def init_inbox() -> Inbox:
    return Inbox(settings.MODULE_NAME)
