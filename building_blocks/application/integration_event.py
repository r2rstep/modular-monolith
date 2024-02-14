from abc import ABC
from typing import TypedDict, TypeVar

from pydantic import ConfigDict, model_validator

from building_blocks.application.notification_event import NotificationEvent
from building_blocks.event import Event


class IntegrationEventDict(TypedDict):
    idempotency_id: str


class IntegrationEventFromNotificationEventDict(IntegrationEventDict, total=False):
    _from_notification_event: bool


class IntegrationEvent(ABC, Event):
    idempotency_id: str

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="before")
    @classmethod
    def ensure_instance_is_crated_from_notification_event(
        cls, data: IntegrationEventFromNotificationEventDict
    ) -> IntegrationEventDict:
        if not data.get("_from_notification_event"):
            raise RuntimeError(
                f"IntegrationEvent instances must be created via"
                f" {IntegrationEvent.from_notification_event.__name__} method."
            )
        del data["_from_notification_event"]
        return data

    @classmethod
    def from_notification_event(cls, notification_event: NotificationEvent) -> "IntegrationEvent":
        integration_event_dict = {k: v for k, v in dict(notification_event).items() if k in cls.model_fields}
        integration_event_dict["_from_notification_event"] = True
        integration_event_dict["idempotency_id"] = notification_event.idempotency_id
        return cls(**integration_event_dict)

    @classmethod
    def event_name(cls) -> str:
        return f"{IntegrationEvent.__name__}__{cls.__name__}"


IntegrationEventType = TypeVar("IntegrationEventType", bound=IntegrationEvent)
