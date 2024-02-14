import typing
from typing import TypedDict
from uuid import uuid4

from pydantic import model_validator

from building_blocks.domain.event import DomainEvent
from building_blocks.event import Event


class NotificationDict(TypedDict):
    idempotency_id: str


class NotificationEvent(Event):
    idempotency_id: str = ""

    @model_validator(mode="before")
    @classmethod
    def initialize_idempotency_id(cls, data: NotificationDict) -> NotificationDict:
        if data.get("idempotency_id") is None:
            data["idempotency_id"] = f"{cls.event_name()}_{uuid4()}"
        return data

    @classmethod
    def from_domain_event(cls, domain_event: DomainEvent) -> "NotificationEvent":
        notification_event_dict = {k: v for k, v in dict(domain_event).items() if k in cls.model_fields}
        return cls(**notification_event_dict)

    @classmethod
    def event_name(cls) -> str:
        return f"{NotificationEvent.__name__}__{cls.__name__}"


NotificationEventType = typing.TypeVar("NotificationEventType", bound=NotificationEvent)
