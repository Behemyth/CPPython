"""TODO"""

from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic.types import DirectoryPath

from cppython.core.schema import CPPythonModel


class ConanData(CPPythonModel):
    """Resolved conan data"""

    tool_directory: Annotated[DirectoryPath, Field()]


class ConanConfiguration(CPPythonModel):
    """Raw conan data"""

    tool_directory: Annotated[Path, Field(default=Path(), description='The directory to place the configuration files')]
