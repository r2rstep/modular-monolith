from collections.abc import Hashable
from typing import Any


class InMemoryDb:
    def __init__(self) -> None:
        self.data: dict[Hashable, Any] = {}

    def set(self, key: Hashable, value: Any) -> None:  # noqa: ANN401, A003
        self.data[key] = value

    def get(self, key: Hashable) -> Any:  # noqa: ANN401
        return self.data.get(key)
