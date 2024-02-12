from abc import ABC, abstractmethod
from typing import Any, Union

from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent


class BoundedContextTranslator(ABC):
    @abstractmethod
    def translate(self, input_: dict[str, Any]) -> Union[DomainEvent, NotificationEvent[DomainEvent]]:
        ...
