import logging
import os
import tempfile
from typing import List, Optional
from pathlib import Path

from eth_utils import keccak
from eth_typing import Address

from besu_plugin import BesuPlugin
from test_pico_cli_plugin import TestPicoCLIPlugin


logger = logging.getLogger(__name__)


class BesuPluginContextImplTest:
    @classmethod
    def create_fake_plugin_dir(cls):
        if "besu.plugins.dir" not in os.environ:
            plugin_dir = tempfile.mkdtemp(prefix="besuTest")
            os.environ["besu.plugins.dir"] = plugin_dir

    def setup_method(self, method):
        os.environ["testPicoCLIPlugin.testOption"] = ""

    def test_verify_everything_goes_smoothly(self):
        context_impl = BesuPluginContextImpl()

        assert len(context_impl.get_plugins()) == 0
        context_impl.register_plugins(Path("."))
        assert len(context_impl.get_plugins()) > 0

        test_plugin_optional = self.find_test_plugin(context_impl.get_plugins())
        assert test_plugin_optional is not None
        test_pico_cli_plugin = test_plugin_optional
        assert test_pico_cli_plugin.get_state() == "registered"

        context_impl.before_external_services()
        context_impl.start_plugins()
        assert test_pico_cli_plugin.get_state() == "started"

        context_impl.stop_plugins()
        assert test_pico_cli_plugin.get_state() == "stopped"

    def test_registration_errors_handled_smoothly(self):
        context_impl = BesuPluginContextImpl()
        os.environ["testPicoCLIPlugin.testOption"] = "FAILREGISTER"

        assert len(context_impl.get_plugins()) == 0
        context_impl.register_plugins(Path("."))
        assert not isinstance(context_impl.get_plugins(), TestPicoCLIPlugin)

        context_impl.before_external_services()
        assert not isinstance(context_impl.get_plugins(), TestPicoCLIPlugin)

        context_impl.start_plugins()
        assert not isinstance(context_impl.get_plugins(), TestPicoCLIPlugin)

        context_impl.stop_plugins()
        assert not isinstance(context_impl.get_plugins(), TestPicoCLIPlugin)

    def test_start_errors_handled_smoothly(self):
        context_impl = BesuPluginContextImpl()
        os.environ["testPicoCLIPlugin.testOption"] = "FAILSTART"

        assert len(context_impl.get_plugins()) == 0
        context_impl.register_plugins(Path("."))
        assert TestPicoCLIPlugin in [
            type(plugin) for plugin in context_impl.get_plugins()
        ]

        test_plugin_optional = self.find_test_plugin(context_impl.get_plugins())
        assert test_plugin_optional is not None
        test_pico_cli_plugin = test_plugin_optional
        assert test_pico_cli_plugin.get_state() == "registered"

        context_impl.before_external_services()
        context_impl.start_plugins()
        assert test_pico_cli_plugin.get_state() == "failstart"
        assert not isinstance(context_impl.get_plugins(), TestPicoCLIPlugin)

        context_impl.stop_plugins()
        assert not isinstance(context_impl.get_plugins(), TestPicoCLIPlugin)

    def test_stop_errors_handled_smoothly(self):
        context_impl = BesuPluginContextImpl()
        os.environ["testPicoCLIPlugin.testOption"] = "FAILSTOP"

        assert len(context_impl.get_plugins()) == 0
        context_impl.register_plugins(Path("."))
        assert TestPicoCLIPlugin in [
            type(plugin) for plugin in context_impl.get_plugins()
        ]

        test_plugin_optional = self.find_test_plugin(context_impl.get_plugins())
        assert test_plugin_optional is not None
        test_pico_cli_plugin = test
