def get_module_name_from_file_path(module_path: str) -> str:
    module_path = module_path[module_path.find("modules") :]
    module_path = module_path.lstrip("modules").lstrip("/")
    return module_path.replace("/", ".")


def get_python_module_from_file_path(module_path: str) -> str:
    module_path = module_path[module_path.find("modules") :]
    return module_path.replace("/", ".")
