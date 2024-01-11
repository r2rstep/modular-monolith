from typing import NewType, Optional, TypeVar
from uuid import UUID

from typing_extensions import TypeAlias

PK = NewType("PK", UUID)

SomeType = TypeVar("SomeType")
NoneOr: TypeAlias = Optional[SomeType]
