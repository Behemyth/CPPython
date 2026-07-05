"""Data definitions for the console application"""

from pydantic import ConfigDict

from cppython.core.schema import CPPythonModel, ProjectConfiguration


class ConsoleConfiguration(CPPythonModel):
    """Configuration data for the console application"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    project_configuration: ProjectConfiguration
