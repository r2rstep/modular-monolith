import sys

if sys.version_info >= (3, 10):
    import inspect

    def get_annotations(cls: type) -> dict[str, type]:
        return inspect.get_annotations(cls)
else:

    def get_annotations(cls: type) -> dict[str, type]:
        return cls.__annotations__
