from abc import ABC, abstractmethod

class PluginServiceFactory(ABC):
    @abstractmethod
    def append_plugin_services(self, besu_context):
        pass
