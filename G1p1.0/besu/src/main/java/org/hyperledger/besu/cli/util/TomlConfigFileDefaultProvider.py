import toml
import os


class TomlConfigFileDefaultProvider:
    def __init__(self, command_line, config_file):
        self.command_line = command_line
        self.config_file = config_file
        self.result = None

    def default_value(self, arg_spec):
        self.load_configuration_from_file()

        if arg_spec.is_option():
            return self.get_configuration_value(arg_spec)
        else:
            return None

    def get_configuration_value(self, option_spec):
        key_name = self.get_key_name(option_spec)

        if key_name is not None:
            if isinstance(option_spec.type(), bool):
                return str(self.result.get(key_name, default=None))
            elif option_spec.is_multi_value() or self.result.is_array(key_name):
                return self.decode_toml_array(self.result.get(key_name, default=None))
            elif isinstance(option_spec.type(), (int, float)):
                return str(self.result.get(key_name, default=None))
            else:
                return str(self.result.get(key_name, default=None))
        else:
            return None

    def get_key_name(self, option_spec):
        for name in option_spec.names():
            name = name.lstrip("-")
            if name in self.result:
                return name
        return None

    def decode_toml_array(self, toml_array_elements):
        if toml_array_elements is None:
            return None
        return ",".join(map(str, toml_array_elements))

    def check_configuration_validity(self):
        if self.result is None or len(self.result) == 0:
            raise ValueError(f"Unable to read TOML configuration file: {self.config_file}")

    def load_configuration_from_file(self):
        if self.result is None:
            if not os.path.isfile(self.config_file):
                raise ValueError(f"Unable to read TOML configuration, file not found: {self.config_file}")

            try:
                self.result = toml.load(self.config_file)

                if "errors" in self.result:
                    errors = "\n".join(self.result["errors"])
                    raise ValueError(f"Invalid TOML configuration: {errors}")

                self.check_unknown_options()

            except IOError:
                raise ValueError(f"Unable to read TOML configuration, file not found: {self.config_file}")

        self.check_configuration_validity()

    def check_unknown_options(self):
        command_spec = self.command_line.get_command_spec()
        unknown_options_list = [option for option in self.result.keys() if "--" + option not in command_spec.options_map]

        if unknown_options_list:
            options = "options" if len(unknown_options_list) > 1 else "option"
            csv_unknown_options = ", ".join(unknown_options_list)
            raise ValueError(f"Unknown {options} in TOML configuration file: {csv_unknown_options}")
