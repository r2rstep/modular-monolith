import typing
from typing import Generic, TypedDict, Union
from uuid import uuid4

from pydantic import ConfigDict, SerializeAsAny, field_validator, model_validator

from building_blocks.domain.event import DomainEvent, DomainEventType
from building_blocks.event import Event


class NotificationDict(TypedDict):
    domain_event: SerializeAsAny[DomainEvent]
    idempotency_id: str


class NotificationEvent(Generic[DomainEventType], Event):
    domain_event: SerializeAsAny[DomainEventType]
    idempotency_id: str = ""

    model_config = ConfigDict(frozen=True)

    @field_validator("domain_event", mode="before")
    @classmethod
    def domain_event_needs_to_be_public(cls, event: DomainEventType) -> DomainEventType:
        if not event.is_public:
            raise ValueError("Domain event needs to be public")
        return event

    @model_validator(mode="before")
    @classmethod
    def initialize_idempotency_id(cls, data: NotificationDict) -> NotificationDict:
        if data.get("idempotency_id") is None:
            data["idempotency_id"] = f"{data['domain_event'].event_name()}_{uuid4()}"
        return data

    @classmethod
    def event_name(cls) -> str:
        raise NotImplementedError(
            "Not possible to implement this method in a generic class."
            " See https://github.com/python/typing/issues/629"
        )

    @staticmethod
    def get_event_name(
        notification: Union["NotificationEvent[DomainEventType]", type["NotificationEvent[DomainEventType]"]]
    ) -> str:
        if isinstance(notification, NotificationEvent):
            domain_event_cls = notification.domain_event.__class__
        else:
            domain_event_cls = typing.get_args(notification)[0]

        return f"{NotificationEvent.__name__}__{domain_event_cls.__name__}"
