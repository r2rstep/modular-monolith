from commons.messagebox.application.process_messagebox_commands import (
    ProcessInbox as ProcessInboxBase,
    ProcessOutbox as ProcessOutboxBase,
)


# cannot inherit from core.application.bases.Command because of circular dependencies
class ProcessOutbox(ProcessOutboxBase):
    ...


# cannot inherit from core.application.bases.Command because of circular dependencies
class ProcessInbox(ProcessInboxBase):
    ...
