"""Test data resolution"""

from pathlib import Path
from typing import Annotated

import pytest
from pydantic import Field

from cppython.core.exception import ConfigException
from cppython.core.plugin_schema.generator import Generator
from cppython.core.plugin_schema.provider import Provider
from cppython.core.plugin_schema.scm import SCM
from cppython.core.resolution import (
    PluginCPPythonData,
    resolve_cppython,
    resolve_cppython_plugin,
    resolve_generator,
    resolve_model,
    resolve_pep621,
    resolve_project_configuration,
    resolve_provider,
    resolve_scm,
)
from cppython.core.schema import (
    CPPythonGlobalConfiguration,
    CPPythonLocalConfiguration,
    CPPythonModel,
    PEP621Configuration,
    ProjectConfiguration,
    ProjectData,
)
from cppython.test.schema import Variant
from cppython.utility.utility import TypeName


class TestResolve:
    """Test resolution of data"""

    @staticmethod
    def test_pep621_resolve(project_configuration: Variant[ProjectConfiguration]) -> None:
        """Test the PEP621 schema resolve function"""
        data = PEP621Configuration(name='pep621-resolve-test', dynamic=['version'])
        resolved = resolve_pep621(data, project_configuration.configuration, None)

        class_variables = vars(resolved)

        assert class_variables
        assert None not in class_variables.values()

    @staticmethod
    def test_project_resolve(project_configuration: Variant[ProjectConfiguration]) -> None:
        """Tests project configuration resolution"""
        assert resolve_project_configuration(project_configuration.configuration)

    @staticmethod
    def test_cppython_resolve(project_configuration: Variant[ProjectConfiguration]) -> None:
        """Tests cppython configuration resolution"""
        cppython_local_configuration = CPPythonLocalConfiguration()
        cppython_global_configuration = CPPythonGlobalConfiguration()

        project_data = resolve_project_configuration(project_configuration.configuration)

        plugin_build_data = PluginCPPythonData(
            generator_name=TypeName('generator'), provider_name=TypeName('provider'), scm_name=TypeName('scm')
        )

        cppython_data = resolve_cppython(
            cppython_local_configuration, cppython_global_configuration, project_data, plugin_build_data
        )

        assert cppython_data

    @staticmethod
    def test_model_resolve() -> None:
        """Test model resolution"""

        class MockModel(CPPythonModel):
            """Mock model for testing"""

            field: Annotated[str, Field()]

        bad_data = {'field': 4}

        with pytest.raises(ConfigException) as error:
            resolve_model(MockModel, bad_data)

        assert error.value.error_count == 1

        good_data = {'field': 'good'}

        resolve_model(MockModel, good_data)

    @staticmethod
    def test_generator_resolve(project_configuration: Variant[ProjectConfiguration]) -> None:
        """Test generator resolution"""
        project_data = ProjectData(project_root=Path())
        cppython_local_configuration = CPPythonLocalConfiguration()
        cppython_global_configuration = CPPythonGlobalConfiguration()

        project_data = resolve_project_configuration(project_configuration.configuration)

        plugin_build_data = PluginCPPythonData(
            generator_name=TypeName('generator'), provider_name=TypeName('provider'), scm_name=TypeName('scm')
        )

        cppython_data = resolve_cppython(
            cppython_local_configuration, cppython_global_configuration, project_data, plugin_build_data
        )

        MockGenerator = type('MockGenerator', (Generator,), {})

        cppython_plugin_data = resolve_cppython_plugin(cppython_data, MockGenerator)

        assert resolve_generator(project_data, cppython_plugin_data)

    @staticmethod
    def test_provider_resolve(project_configuration: Variant[ProjectConfiguration]) -> None:
        """Test provider resolution"""
        project_data = ProjectData(project_root=Path())
        cppython_local_configuration = CPPythonLocalConfiguration()
        cppython_global_configuration = CPPythonGlobalConfiguration()

        project_data = resolve_project_configuration(project_configuration.configuration)

        plugin_build_data = PluginCPPythonData(
            generator_name=TypeName('generator'), provider_name=TypeName('provider'), scm_name=TypeName('scm')
        )

        cppython_data = resolve_cppython(
            cppython_local_configuration, cppython_global_configuration, project_data, plugin_build_data
        )

        MockProvider = type('MockProvider', (Provider,), {})

        cppython_plugin_data = resolve_cppython_plugin(cppython_data, MockProvider)

        assert resolve_provider(project_data, cppython_plugin_data)

    @staticmethod
    def test_scm_resolve(project_configuration: Variant[ProjectConfiguration]) -> None:
        """Test scm resolution"""
        project_data = ProjectData(project_root=Path())
        cppython_local_configuration = CPPythonLocalConfiguration()
        cppython_global_configuration = CPPythonGlobalConfiguration()

        project_data = resolve_project_configuration(project_configuration.configuration)

        plugin_build_data = PluginCPPythonData(
            generator_name=TypeName('generator'), provider_name=TypeName('provider'), scm_name=TypeName('scm')
        )

        cppython_data = resolve_cppython(
            cppython_local_configuration, cppython_global_configuration, project_data, plugin_build_data
        )

        MockSCM = type('MockSCM', (SCM,), {})

        cppython_plugin_data = resolve_cppython_plugin(cppython_data, MockSCM)

        assert resolve_scm(project_data, cppython_plugin_data)
