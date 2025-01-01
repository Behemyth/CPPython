"""_summary_"""

from pathlib import Path
from typing import Any

import requests

from cppython.core.plugin_schema.generator import SyncConsumer
from cppython.core.plugin_schema.provider import Provider, ProviderPluginGroupData, SupportedProviderFeatures
from cppython.core.schema import CorePluginData, Information, SyncData
from cppython.plugins.cmake.plugin import CMakeGenerator
from cppython.plugins.cmake.schema import CMakeSyncData
from cppython.plugins.conan.resolution import resolve_conan_data
from cppython.plugins.conan.schema import ConanData
from cppython.utility.exception import NotSupportedError
from cppython.utility.utility import TypeName


class ConanProvider(Provider):
    """Conan Provider"""

    def __init__(
        self, group_data: ProviderPluginGroupData, core_data: CorePluginData, configuration_data: dict[str, Any]
    ) -> None:
        """Initializes the provider"""
        self.group_data: ProviderPluginGroupData = group_data
        self.core_data: CorePluginData = core_data
        self.data: ConanData = resolve_conan_data(configuration_data, core_data)

        self._provider_file = self.core_data.cppython_data.tool_path / 'conan' / 'conan_provider.cmake'
        self._provider_url = (
            'https://raw.githubusercontent.com/conan-io/cmake-conan/refs/heads/develop2/conan_provider.cmake'
        )

    @staticmethod
    def _download_file(url: str, file: Path) -> None:
        """Replaces the given file with the contents of the url"""
        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, 'wb') as out_file:
            content = requests.get(url, stream=True).content
            out_file.write(content)

    @staticmethod
    def features(directory: Path) -> SupportedProviderFeatures:
        """Queries conan support

        Args:
            directory: The directory to query

        Returns:
            Supported features
        """
        return SupportedProviderFeatures()

    @staticmethod
    def information() -> Information:
        """Returns plugin information

        Returns:
            Plugin information
        """
        return Information()

    def install(self) -> None:
        """Installs the provider"""
        self._download_file(
            self._provider_url,
            self._provider_file,
        )

    def update(self) -> None:
        """Updates the provider"""
        self._download_file(
            self._provider_url,
            self._provider_file,
        )

    @staticmethod
    def supported_sync_type(sync_type: type[SyncData]) -> bool:
        """_summary_

        Args:
            sync_type: _description_

        Returns:
            _description_
        """
        return sync_type in CMakeGenerator.sync_types()

    def sync_data(self, consumer: SyncConsumer) -> SyncData:
        """_summary_

        Args:
            consumer: _description_

        Returns:
            _description_
        """
        for sync_type in consumer.sync_types():
            if sync_type == CMakeSyncData:
                return CMakeSyncData(provider_name=TypeName('conan'), top_level_includes=self._provider_file)

        raise NotSupportedError('OOF')