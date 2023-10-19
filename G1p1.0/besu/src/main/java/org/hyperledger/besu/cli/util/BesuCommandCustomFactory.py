import importlib

class BesuCommandCustomFactory:
    def __init__(self, plugin_versions_provider):
        self.plugin_versions_provider = plugin_versions_provider
        self.default_factory = CommandLine.defaultFactory()

    def create(self, cls):
        if issubclass(cls, CommandLine.IVersionProvider):
            version_provider_module = importlib.import_module("version_provider_module")
            version_provider = version_provider_module.VersionProvider(self.plugin_versions_provider)
            return version_provider

        return self.default_factory.create(cls)
