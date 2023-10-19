from typing import Any
from eth_keys import keys
from eth_utils import to_checksum_address
from eth_utils.typing import ChecksumAddress
from eth_typing import HexStr
from eth.vm.forks.frontier.blocks import FrontierBlock
from eth.vm.forks.frontier.computation import FrontierComputation
from eth.vm.forks.frontier.state import FrontierState
from eth.vm.forks.frontier.vm import FrontierVM
from eth.vm.forks.homestead import HomesteadVM
from eth.vm.state import BaseState
from eth.vm.transaction_context import BaseTransactionContext
from eth._utils.datatypes import (
    Configurable,
    PropertyCheckingFactory,
    NoopNormalization,
)
from eth.vm.base import VM

from eth_hash.auto import keccak

from eth_keys.exceptions import (
    BadSignature,
    ValidationError,
)
from eth_utils.toolz import assoc

import rlp

from trie import HexaryTrie

from eth_utils import to_dict
from typing import Dict, Type, TypeVar

from eth_utils.typing import (
    Address,
    Hash32,
)
from eth_utils import to_checksum_address
from rlp.sedes import (
    binary,
    big_endian_int,
    binary,
    CountableList,
    int256,
    int32,
    big_endian_int,
)

from rlp import (
    DecodingError,
    EncodingError,
    encode,
)

from eth_utils import to_dict


def publicKeyToAddress(public_key: HexStr) -> ChecksumAddress:
    pk = keys.PublicKey(public_key)
    address = to_checksum_address(pk.to_canonical_address())
    return address


def installCliqueBlockChoiceRule(blockchain: Any, cliqueContext: Any) -> None:
    pass


class CliqueConfigOptions(Configurable):
    def __init__(self, epoch_length: int, block_period_seconds: int) -> None:
        self.epoch_length = epoch_length
        self.block_period_seconds = block_period_seconds


class CliqueBlockInterface:
    def validatorsInBlock(self, blockHeader: Any) -> Any:
        pass


class CliqueJsonRpcMethods:
    def __init__(self, protocolContext: Any) -> None:
        pass


class CliqueMinerExecutor:
    def __init__(
        self,
        protocolContext: Any,
        protocolSchedule: Any,
        pendingTransactions: Any,
        nodeKey: Any,
        miningParameters: Any,
        cliqueBlockScheduler: Any,
        epochManager: Any,
    ) -> None:
        pass


class CliqueMiningTracker:
    def __init__(self, localAddress: Any, protocolContext: Any) -> None:
        pass


class CliqueMiningCoordinator:
    def __init__(
        self,
        blockchain: Any,
        miningExecutor: Any,
        syncState: Any,
        miningTracker: Any,
    ) -> None:
        pass


class CliqueBesuControllerBuilder:
    def __init__(self) -> None:
        self.localAddress = None
        self.epochManager = None
        self.secondsBetweenBlocks = None
        self.blockInterface = CliqueBlockInterface()

    def prepForBuild(self) -> None:
        self.localAddress = publicKeyToAddress(nodeKey.getPublicKey())
        cliqueConfig = configOptionsSupplier.get().getCliqueConfigOptions()
        blocksPerEpoch = cliqueConfig.epoch_length
        self.secondsBetweenBlocks = cliqueConfig.block_period_seconds

        self.epochManager = EpochManager(blocksPerEpoch)

    def createAdditionalJsonRpcMethodFactory(
        self, protocolContext: Any
    ) -> CliqueJsonRpcMethods:
        return CliqueJsonRpcMethods(protocolContext)

   
