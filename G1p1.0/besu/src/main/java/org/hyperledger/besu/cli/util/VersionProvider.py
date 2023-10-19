from typing import List
from besu import BesuInfo
from besu.plugin.services import PluginVersionsProvider


class VersionProvider:
    def __init__(self, plugin_versions_provider: PluginVersionsProvider):
        self.plugin_versions_provider = plugin_versions_provider

    def get_version(self) -> List[str]:
        versions = [BesuInfo.version()] + self.plugin_versions_provider.get_plugin_versions()
        return versions
