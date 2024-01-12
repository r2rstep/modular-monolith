from dataclasses import dataclass
from datetime import datetime
from typing import Any, NewType, TypedDict

from commons.types import NoneOr

MessageName = NewType("MessageName", str)


@dataclass
class MessageDTO:
    name: MessageName
    payload: dict[str, Any]


class MessageDict(TypedDict):
    name: MessageName
    payload: dict[str, object]
    status: str
    created_at: datetime


class Messagebox:
    def __init__(self, module_name: str):
        self._messagebox_name = f"{module_name.replace('.', '_')}_messagebox"
        self._messagebox: list[MessageDict] = []

    async def add(self, name: MessageName, payload: dict[str, object]) -> None:
        self._messagebox.append(
            {"name": name, "payload": payload, "status": "pending", "created_at": datetime.utcnow()}
        )

    async def get_next(self) -> NoneOr[MessageDTO]:
        if self._messagebox:
            entry = self._messagebox.pop(0)
            return MessageDTO(entry["name"], entry["payload"])
        return None


class Outbox(Messagebox):
    def __init__(self, module_name: str):
        super().__init__(module_name)

        self._outbox_name = f"{module_name.replace('.', '_')}_outbox"


class Inbox(Messagebox):
    def __init__(self, module_name: str):
        super().__init__(module_name)

        self._messagebox_name = f"{module_name.replace('.', '_')}_inbox"

    async def add_idempotent(self, name: MessageName, payload: dict[str, object], idempotence_id: str) -> None:
        if not any(message["payload"].get("__idempotent_id") == idempotence_id for message in self._messagebox):
            payload["__idempotent_id"] = idempotence_id
            await self.add(name, payload)

    async def get_next(self) -> NoneOr[MessageDTO]:
        if message := await super().get_next():
            message.payload.pop("__idempotent_id", None)
            return message
        return None
