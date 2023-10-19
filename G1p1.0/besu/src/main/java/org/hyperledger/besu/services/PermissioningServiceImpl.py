import logging
import os
from typing import Any, Dict, List, Optional, Type, Union

from .besu_service import BesuService
from .besu_plugin import BesuPlugin
from .plugin_versions_provider import PluginVersionsProvider


class Lifecycle:
    UNINITIALIZED = 0
    REGISTERING = 1
    REGISTERED = 2
    BEFORE_EXTERNAL_SERVICES_STARTED = 3
    BEFORE_EXTERNAL_SERVICES_FINISHED = 4
    BEFORE_MAIN_LOOP_STARTED = 5
    BEFORE_MAIN_LOOP_FINISHED = 6
    STOPPING = 7
    STOPPED = 8


class BesuPluginContextImpl:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.state = Lifecycle.UNINITIALIZED
        self.service_registry = {}
        self.plugins = []
        self.plugin_versions = []

    def add_service(self, service_type: Type[BesuService], service: BesuService) -> None:
        if not issubclass(service_type, BesuService):
            raise ValueError("Services must be subclasses of BesuService.")
        if not isinstance(service, service_type):
            raise ValueError("The service registered with a type must be an instance of that type.")
        self.service_registry[service_type] = service

    def get_service(self, service_type: Type[BesuService]) -> Optional[BesuService]:
        return self.service_registry.get(service_type)

    def register_plugins(self, plugins_dir: str) -> None:
        if self.state != Lifecycle.UNINITIALIZED:
            raise RuntimeError("Besu plugins have already been registered.")

        plugin_loader = self._plugin_directory_loader(plugins_dir) or __loader__

        self.state = Lifecycle.REGISTERING

        plugin_classes = plugin_loader.load_plugins()
        for plugin_class in plugin_classes:
            try:
                plugin = plugin_class()
                plugin.register(self)
                self.logger.debug("Registered plugin of type {}.".format(plugin_class.__name__))
                self._add_plugin_version(plugin)
                self.plugins.append(plugin)
            except Exception as e:
                self.logger.error(
                    "Error registering plugin of type {}, start and stop will not be called.".format(
                        plugin_class.__name__
                    ),
                    exc_info=e,
                )
                continue

        self.logger.debug("Plugin registration complete.")
        self.state = Lifecycle.REGISTERED

    def _add_plugin_version(self, plugin: BesuPlugin) -> None:
        plugin_module = plugin.__class__.__module__
        plugin_class = plugin.__class__.__name__
        plugin_version = f"{plugin_module}/{plugin_class}"
        self.plugin_versions.append(plugin_version)

    def before_external_services(self) -> None:
        if self.state != Lifecycle.REGISTERED:
            raise RuntimeError(
                "BesuContext should be in state REGISTERED but it was in {}".format(self.state)
            )
        self.state = Lifecycle.BEFORE_EXTERNAL_SERVICES_STARTED

        for plugin in self.plugins[:]:
            try:
                plugin.before_external_services()
                self.logger.debug(
                    "before_external_services called on plugin of type {}.".format(
                        plugin.__class__.__name__
                    )
                )
            except Exception as e:
                self.logger.error(
                    "Error calling `before_external_services` on plugin of type {}, "
                    "stop will not be called.".format(plugin.__class__.__name__),
                    exc_info=e,
                )
                self.plugins.remove(plugin)

        self.logger.debug("Plugin startup complete.")
        self.state = Lifecycle.BEFORE_EXTERNAL_SERVICES_FINISHED

    def start_plugins
