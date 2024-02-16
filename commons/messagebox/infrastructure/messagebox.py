from collections.abc import Awaitable, Iterator
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Callable, Literal, NewType, TypedDict, TypeVar, cast

from typing_extensions import ParamSpec

from commons.types import NoneOr

MessageTopic = NewType("MessageTopic", str)


MessagePayload = dict[str, Any]


class MessageDict(TypedDict):
    topic: MessageTopic
    payload: MessagePayload
    status: Literal["pending", "processed"]
    created_at: datetime


FuncParams = ParamSpec("FuncParams")
ReturnType = TypeVar("ReturnType")


def _verify_is_opened(fn: Callable[FuncParams, Awaitable[ReturnType]]) -> Callable[FuncParams, Awaitable[ReturnType]]:
    async def wrapper(*args: "FuncParams.args", **kwargs: "FuncParams.kwargs") -> "ReturnType":
        if not cast(Messagebox, args[0])._opened:  # noqa: SLF001
            raise RuntimeError(f"Messagebox needs to be opened before calling {fn.__name__}")
        return await fn(*args, **kwargs)

    return wrapper


class Messagebox:
    def __init__(self, module_name: str):
        self._messagebox_name = f"{module_name.replace('.', '_')}_messagebox"
        self._messagebox: list[MessageDict] = []
        self._locked_messages: list[MessageDict] = []
        self._opened = False

    @contextmanager
    def open(self) -> Iterator[None]:  # noqa: A003
        self._opened = True
        try:
            yield
        finally:
            self._locked_messages.clear()
            self._opened = False

    @_verify_is_opened
    async def add(self, topic: MessageTopic, payload: MessagePayload) -> None:
        self._messagebox.append({"topic": topic, "payload": payload, "status": "pending", "created_at": datetime.now()})

    @_verify_is_opened
    async def get_next_pending(self) -> NoneOr[MessageDict]:
        message = next(
            (
                message
                for message in self._messagebox
                if ((message["status"] == "pending") and (message not in self._locked_messages))
            ),
            None,
        )
        if message:
            self._locked_messages.append(message)
            return message
        return None


class Outbox(Messagebox):
    def __init__(self, module_name: str):
        super().__init__(module_name)

        self._outbox_name = f"{module_name.replace('.', '_')}_outbox"


class Inbox(Messagebox):
    def __init__(self, module_name: str):
        super().__init__(module_name)

        self._messagebox_name = f"{module_name.replace('.', '_')}_inbox"

    async def add_idempotent(self, topic: MessageTopic, payload: MessagePayload, idempotence_id: str) -> None:
        if not any(message["payload"].get("__idempotent_id") == idempotence_id for message in self._messagebox):
            payload["__idempotent_id"] = idempotence_id
            await self.add(topic, payload)

    async def get_next_pending(self) -> NoneOr[MessageDict]:
        if message := await super().get_next_pending():
            message["payload"].pop("__idempotent_id", None)
            return message
        return None
