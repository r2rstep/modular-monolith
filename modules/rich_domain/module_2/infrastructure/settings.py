from pathlib import Path

from building_blocks.within_bounded_context.infrastructure.utils import (
    get_module_name_from_file_path,
    get_python_module_from_file_path,
)

_MODULE_FILE_PATH = Path(__file__).parent.parent
MODULE_NAME = get_module_name_from_file_path(str(_MODULE_FILE_PATH))
MODULE = get_python_module_from_file_path(str(_MODULE_FILE_PATH))
