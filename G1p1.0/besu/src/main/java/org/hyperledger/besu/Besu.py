import logging
import sys

from besu.chainexport import RlpBlockExporter
from besu.chainimport import JsonBlockImporter, RlpBlockImporter
from besu.cli import BesuCommand
from besu.cli.logging import BesuLoggingConfigurationFactory
from besu.controller import BesuController
from besu.services import BesuPluginContextImpl

logger = logging.getLogger(__name__)
SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1


def main(*args):
    setup_logging()

    besu_command = BesuCommand(
        logger,
        RlpBlockImporter,
        JsonBlockImporter,
        RlpBlockExporter,
        RunnerBuilder(),
        BesuController.Builder(),
        BesuPluginContextImpl(),
        dict(os.environ)
    )

    besu_command.parse(
        RunLast().and_exit(SUCCESS_EXIT_CODE),
        besu_command.exception_handler().and_exit(ERROR_EXIT_CODE),
        sys.stdin,
        args
    )


def setup_logging():
    logging.getLogger("io.netty").setLevel(logging.ERROR)
    logging.getLogger("org.hyperledger.besu").setLevel(logging.INFO)

    try:
        import log4j2
        log4j2.set_file_property("log4j2.configurationFactory", BesuLoggingConfigurationFactory)
        log4j2.set_file_property("log4j2.skipJansi", "false")
    except ImportError:
        print("Failed to import log4j2. Please make sure it is installed.")

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


if __name__ == "__main__":
    main(*sys.argv[1:])
