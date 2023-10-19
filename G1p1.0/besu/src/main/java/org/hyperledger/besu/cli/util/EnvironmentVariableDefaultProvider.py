import os
import re
from typing import List
from picocli import IDefaultValueProvider
from picocli import ArgSpec, OptionSpec


class EnvironmentVariableDefaultProvider(IDefaultValueProvider):
    ENV_VAR_PREFIX = "BESU_"
    LEGACY_ENV_VAR_PREFIX = "PANTHEON_"

    def __init__(self, environment):
        self.environment = environment

    def default_value(self, arg_spec: ArgSpec) -> str:
        if isinstance(arg_spec, OptionSpec):
            return self.get_option_default_value(arg_spec)
        return None

    def get_option_default_value(self, option_spec: OptionSpec) -> str:
        env_var_names = self.get_env_var_names(option_spec)
        for env_var in env_var_names:
            if env_var in self.environment:
                return self.environment[env_var]
        return None

    def get_env_var_names(self, option_spec: OptionSpec) -> List[str]:
        names = option_spec.names()
        env_var_names = []
        for name in names:
            if name.startswith("--"):
                env_var_names.extend(self.create_env_var_names(name))
        return env_var_names

    def create_env_var_names(self, name: str) -> List[str]:
        suffix = self.name_to_env_var_suffix(name)
        return [self.ENV_VAR_PREFIX + suffix, self.LEGACY_ENV_VAR_PREFIX + suffix]

    def name_to_env_var_suffix(self, name: str) -> str:
        name_without_prefix = re.sub(r"^--", "", name)
        return name_without_prefix.replace("-", "_").upper()
