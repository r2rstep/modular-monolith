from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from building_blocks.types import NoneOr

MessageName = NewType("MessageName", str)


@dataclass
class MessageDTO:
    name: MessageName
    payload: dict[str, object]


class MessageBox:
    def __init__(self, module_name: str):
        self._outbox_name = f"{module_name.replace('.', '_')}_outbox"
        self._message_box = []

    async def add(self, name: MessageName, payload: dict[str, object]) -> None:
        self._message_box.append(
            {"name": name, "payload": payload, "status": "pending", "created_at": datetime.utcnow()}
        )

    async def get_next(self) -> NoneOr[MessageDTO]:
        if self._message_box:
            entry = self._message_box.pop(0)
            return MessageDTO(entry["name"], entry["payload"])
        return None


class Outbox(MessageBox):
    def __init__(self, module_name: str):
        super().__init__(module_name)

        self._outbox_name = f"{module_name.replace('.', '_')}_outbox"


class Inbox(MessageBox):
    def __init__(self, module_name: str):
        super().__init__(module_name)

        self._outbox_name = f"{module_name.replace('.', '_')}_inbox"
