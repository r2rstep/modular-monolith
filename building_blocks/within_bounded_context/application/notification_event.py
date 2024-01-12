from typing import Generic, TypedDict
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, SerializeAsAny, field_validator, model_validator

from building_blocks.within_bounded_context.domain.events import DomainEvent, DomainEventType


class NotificationDict(TypedDict):
    domain_event: SerializeAsAny[DomainEvent]
    idempotency_id: str


class NotificationEvent(BaseModel, Generic[DomainEventType]):
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
            data["idempotency_id"] = f"{data['domain_event'].name}_{uuid4()}"
        return data
