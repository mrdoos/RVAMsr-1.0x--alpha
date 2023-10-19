import os
import sys
from typing import List, Optional
from abc import ABC, abstractmethod

import argparse


class ConfigOptionSearchAndRunHandler:
    def __init__(
        self,
        result_handler,
        exception_handler,
        environment,
    ):
        self.result_handler = result_handler
        self.exception_handler = exception_handler
        self.environment = environment

    def handle(self, parse_result):
        command_line = parse_result.command_spec().command_line()
        config_file = self.find_config_file(parse_result, command_line)
        self.validate_privacy_options(parse_result, command_line)
        default_value_provider = self.create_default_value_provider(
            command_line, config_file
        )
        command_line.set_default_value_provider(default_value_provider)
        command_line.parse_args(args=sys.argv[1:])
        return []

    def validate_privacy_options(self, parse_result, command_line):
        if (
            parse_result.has_matched_option("--privacy-onchain-groups-enabled")
            and parse_result.has_matched_option("--privacy-flexible-groups-enabled")
        ):
            raise argparse.ArgumentError(
                None,
                "The `--privacy-onchain-groups-enabled` option is deprecated and you should only use `--privacy-flexible-groups-enabled`",
            )

    def find_config_file(self, parse_result, command_line):
        if (
            parse_result.has_matched_option("--config-file")
            and "BESU_CONFIG_FILE" in self.environment
        ):
            raise argparse.ArgumentError(
                None,
                f"TOML file specified using BESU_CONFIG_FILE={self.environment['BESU_CONFIG_FILE']} and --config-file {parse_result.matched_option('--config-file').
