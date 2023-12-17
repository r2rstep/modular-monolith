def get_module_name(_module_path: str) -> str:
    _module_path = _module_path[_module_path.find("modules") :]
    _module_path = _module_path.lstrip("modules").lstrip("/")
    return _module_path.replace("/", ".")
