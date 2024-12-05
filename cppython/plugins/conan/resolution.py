"""_summary_"""

from typing import Any

from cppython.core.schema import CorePluginData
from cppython.plugins.conan.schema import ConanConfiguration, ConanData


def resolve_conan_data(data: dict[str, Any], core_data: CorePluginData) -> ConanData:
    """Resolves the conan data

    Args:
        data: The data to resolve
        core_data: The core plugin data

    Returns:
        The resolved conan data
    """
    parsed_data = ConanConfiguration(**data)
    root_directory = core_data.project_data.pyproject_file.parent.absolute()

    modified_tool_directory = parsed_data.tool_directory

    # Add the project location to all relative paths
    if not modified_tool_directory.is_absolute():
        modified_tool_directory = root_directory / modified_tool_directory

    return ConanData(tool_directory=modified_tool_directory)
