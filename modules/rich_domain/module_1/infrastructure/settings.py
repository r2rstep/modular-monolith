from pathlib import Path

from building_blocks.within_bounded_context.infrastructure.utils import get_module_name

MODULE_NAME = get_module_name(str(Path(__file__).parent.parent))
