import logging
from typing import Any

from picocli import CommandSpec

from .pico_cli_options import PicoCLIOptions

logger = logging.getLogger(__name__)


class PicoCLIOptionsImpl(PicoCLIOptions):
    def __init__(self, command_line: Any):
        self.command_line = command_line

    def add_pico_cli_options(self, namespace: str, option_object: Any) -> None:
        plugin_prefix = f"--plugin-{namespace}-"
        unstable_prefix = f"--Xplugin-{namespace}-"
        mixin = CommandSpec.forAnnotatedObject(option_object)
        bad_option_name = False

        for option_spec in mixin.options():
            for option_name in option_spec.names():
                if not option_name.startswith(plugin_prefix) and not option_name.startswith(unstable_prefix):
                    bad_option_name = True
                    logger.error("Plugin option %s did not have the expected prefix of %s", option_name, plugin_prefix)

        if bad_option_name:
            raise RuntimeError("Error loading CLI options")
        else:
            self.command_line.command_spec.add_mixin(f"Plugin {namespace}", mixin)
