from typing import Dict
from decimal import Decimal

class CliqueConfigOptions:
    DEFAULT_EPOCH_LENGTH = 30_000
    DEFAULT_BLOCK_PERIOD_SECONDS = 15

    def __init__(self, cliqueConfigRoot: Dict):
        self.cliqueConfigRoot = cliqueConfigRoot

    def get_epoch_length(self) -> int:
        return self.cliqueConfigRoot.get("epochlength", self.DEFAULT_EPOCH_LENGTH)

    def get_block_period_seconds(self) -> int:
        return self.cliqueConfigRoot.get("blockperiodseconds", self.DEFAULT_BLOCK_PERIOD_SECONDS)

    def as_map(self) -> Dict[str, object]:
        return {
            "epochLength": self.get_epoch_length(),
            "blockPeriodSeconds": self.get_block_period_seconds(),
        }
