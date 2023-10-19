from typing import List
from picocli import IDefaultValueProvider
from picocli.model import ArgSpec

class CascadingDefaultProvider(IDefaultValueProvider):
    def __init__(self, *default_value_providers: IDefaultValueProvider):
        self.default_value_providers = default_value_providers

    def default_value(self, arg_spec: ArgSpec) -> str:
        for provider in self.default_value_providers:
            default_value = provider.default_value(arg_spec)
            if default_value is not None:
                return default_value
        return None
