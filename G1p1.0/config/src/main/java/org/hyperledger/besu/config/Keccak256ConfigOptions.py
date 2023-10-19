from typing import Optional
from numbers import Number
from collections import OrderedDict


class Keccak256ConfigOptions:
    DEFAULT = None

    def __init__(self, keccak256ConfigRoot):
        self.keccak256ConfigRoot = keccak256ConfigRoot

    def get_fixed_difficulty(self) -> Optional[int]:
        return JsonUtil.get_long(self.keccak256ConfigRoot, "fixeddifficulty")

    def as_map(self):
        builder = OrderedDict()
        fixed_difficulty = self.get_fixed_difficulty()
        if fixed_difficulty is not None:
            builder["fixeddifficulty"] = fixed_difficulty
        return builder


class JsonUtil:
    @staticmethod
    def get_value_as_string(node, key):
        value = node.get(key)
        if value is not None:
            return str(value)
        return None

    @staticmethod
    def get_long(node, key):
        value = node.get(key)
        if isinstance(value, Number) and int(value) != value:
            return int(value)
        return None
