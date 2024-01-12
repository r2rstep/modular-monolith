import sys
from typing import Protocol, TypeVar, cast

if sys.version_info >= (3, 10):
    import inspect

    def get_annotations(cls: type) -> dict[str, type]:
        return inspect.get_annotations(cls)
else:

    def get_annotations(cls: type) -> dict[str, type]:
        return cls.__annotations__


ClassType = TypeVar("ClassType")


class ClassProtocol(Protocol[ClassType]):
    @classmethod
    def __subclasses__(cls) -> list[type[ClassType]]:
        ...


def get_all_subclasses(cls: type[ClassProtocol[ClassType]]) -> list[type[ClassType]]:
    return cls.__subclasses__() + [
        g for s in cls.__subclasses__() for g in get_all_subclasses(cast(type[ClassProtocol[ClassType]], s))
    ]
