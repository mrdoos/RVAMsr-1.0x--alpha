import logging
from typing import List
from picocli import CommandLine
from picocli.model import OptionSpec
from functools import reduce
from operator import itemgetter


class CommandLineUtils:
    DEPENDENCY_WARNING_MSG = "{} has been ignored because {} was not defined on the command line."
    MULTI_DEPENDENCY_WARNING_MSG = "{} ignored because none of {} was defined."
    DEPRECATION_WARNING_MSG = "{} has been deprecated, use {} instead."
    DEPRECATED_AND_USELESS_WARNING_MSG = "{} has been deprecated and is now useless, remove it."

    @staticmethod
    def check_option_dependencies(logger: logging.Logger, command_line: CommandLine, main_option_name: str,
                                  is_main_option_condition: bool, dependent_options_names: List[str]):
        if is_main_option_condition:
            affected_options = CommandLineUtils.get_affected_options(command_line, dependent_options_names)

            if affected_options:
                logger.warning(CommandLineUtils.DEPENDENCY_WARNING_MSG.format(affected_options, main_option_name))

    @staticmethod
    def check_multi_option_dependencies(logger: logging.Logger, command_line: CommandLine, string_to_log: str,
                                        is_main_option_condition: List[bool], dependent_options_names: List[str]):
        if all(is_main_option_condition):
            affected_options = CommandLineUtils.get_affected_options(command_line, dependent_options_names)

            if affected_options:
                logger.warning(string_to_log)

    @staticmethod
    def get_affected_options(command_line: CommandLine, dependent_options_names: List[str]) -> str:
        options = command_line.get_command_spec().options()
        affected_options = [option.names()[0] for option in options
                            if any(name in dependent_options_names for name in option.names())
                            and option.string_values()]

        return reduce(lambda x, y: f"{x}, {y}", affected_options)


# Exemplo de uso:
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    command_line = CommandLine()

    main_option_name = "--main-option"
    is_main_option_condition = True
    dependent_options_names = ["--dependent-option1", "--dependent-option2"]

    CommandLine
