"""Data schemas for plugin testing"""

from typing import Annotated

from pydantic import Field

from cppython.core.schema import CPPythonModel


class Variant[T: CPPythonModel](CPPythonModel):
    """A configuration variant for a schema type"""

    configuration: Annotated[T, Field(description='The configuration data')]


class Variants[T: CPPythonModel](CPPythonModel):
    """A group of variants"""

    variants: Annotated[list[Variant[T]], Field(description='Data variants')] = []
