import json
from typing import Optional, Union
from numbers import Number


class JsonUtil:
    @staticmethod
    def normalize_keys(object_node):
        normalized = {}
        for key, value in object_node.items():
            normalized_key = key.lower()
            if isinstance(value, dict):
                normalized[normalized_key] = JsonUtil.normalize_keys(value)
            elif isinstance(value, list):
                normalized[normalized_key] = JsonUtil.normalize_keys_in_array(value)
            else:
                normalized[normalized_key] = value
        return normalized

    @staticmethod
    def normalize_keys_in_array(array_node):
        normalized_array = []
        for value in array_node:
            if isinstance(value, dict):
                normalized_array.append(JsonUtil.normalize_keys(value))
            elif isinstance(value, list):
                normalized_array.append(JsonUtil.normalize_keys_in_array(value))
            else:
                normalized_array.append(value)
        return normalized_array

    @staticmethod
    def get_value_as_string(node, key):
        value = node.get(key)
        if value is not None:
            return str(value)
        return None

    @staticmethod
    def get_string(node, key, default_value=None):
        value = JsonUtil.get_value_as_string(node, key)
        return value if value is not None else default_value

    @staticmethod
    def has_key(node, key):
        return key in node

    @staticmethod
    def get_int(node, key):
        value = node.get(key)
        if isinstance(value, Number) and int(value) == value:
            return int(value)
        return None

    @staticmethod
    def get_positive_int(node, key):
        value = JsonUtil.get_value_as_string(node, key)
        if value is not None:
            try:
                parsed_value = int(value)
                if parsed_value > 0:
                    return parsed_value
            except ValueError:
                pass
        return None

    @staticmethod
    def get_long(node, key):
        value = node.get(key)
        if isinstance(value, Number) and int(value) != value:
            return int(value)
        return None

    @staticmethod
    def get_boolean(node, key):
        value = node.get(key)
        if isinstance(value, bool):
            return value
        return None

    @staticmethod
    def create_empty_object_node():
        return {}

    @staticmethod
    def create_empty_array_node():
        return []

    @staticmethod
    def object_node_from_map(map_obj):
        return dict(map_obj)

    @staticmethod
    def object_node_from_string(json_data):
        return json.loads(json_data)

    @staticmethod
    def get_json(object_node, pretty_print=True):
        if pretty_print:
            return json.dumps(object_node, indent=4)
        return json.dumps(object_node)

    @staticmethod
    def get_object_node(json, field_key, strict=True):
        value = json.get(field_key)
        if value is not None:
            if isinstance(value, dict):
                return value
            elif not strict:
                return None
        return None

    @staticmethod
    def get_array_node(json, field_key, strict=True):
        value = json.get(field_key)
        if value is not None:
            if isinstance(value, list):
                return value
            elif not strict:
                return None
        return None
