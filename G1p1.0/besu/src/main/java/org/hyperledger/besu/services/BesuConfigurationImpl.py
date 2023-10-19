from typing import List, Optional, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from org.hyperledger.besu.config import GenesisConfigFile
from org.hyperledger.besu.consensus.merge import (
    PostMergeContext,
    TransitionBackwardSyncContext,
    TransitionContext,
    TransitionProtocolSchedule,
)
from org.hyperledger.besu.consensus.merge.blockcreation import TransitionCoordinator
from org.hyperledger.besu.consensus.qbft.pki import PkiBlockCreationConfiguration
from org.hyperledger.besu.controller import BesuControllerBuilder
from org.hyperledger.besu.crypto import NodeKey
from org.hyperledger.besu.datatypes import Hash
from org.hyperledger.besu.ethereum import (
    ConsensusContext,
    GasLimitCalculator,
    MiningParameters,
    ProtocolContext,
)
from org.hyperledger.besu.ethereum.blockcreation import MiningCoordinator
from org.hyperledger.besu.ethereum.chain import Blockchain
from org.hyperledger.besu.ethereum.core import MiningParameters
from org.hyperledger.besu.ethereum.eth import EthProtocolConfiguration
from org.hyperledger.besu.ethereum.eth.manager import EthProtocolManager
from org.hyperledger.besu.ethereum.eth.sync import SynchronizerConfiguration
from org.hyperledger.besu.ethereum.eth.sync.backwardsync import BackwardSyncContext
from org.hyperledger.besu.ethereum.eth.sync.state import SyncState
from org.hyperledger.besu.ethereum.eth.transactions import TransactionPool
from org.hyperledger.besu.ethereum.eth.transactions import TransactionPoolConfiguration
from org.hyperledger.besu.ethereum.mainnet import ProtocolSchedule
from org.hyperledger.besu.ethereum.storage import StorageProvider
from org.hyperledger.besu.ethereum.worldstate import (
    DataStorageConfiguration,
    PrunerConfiguration,
    WorldStateArchive,
)
from org.hyperledger.besu.evm.internal import EvmConfiguration
from org.hyperledger.besu.metrics import ObservableMetricsSystem
from org.hyperledger.besu.plugin.services.permissioning import NodeMessagePermissioningProvider

from java.math import BigInteger


class TransitionBesuControllerBuilder(BesuControllerBuilder):
    def __init__(
        self,
        pre_merge_besu_controller_builder: BesuControllerBuilder,
        merge_besu_controller_builder: MergeBesuControllerBuilder,
    ):
        self.pre_merge_besu_controller_builder = pre_merge_besu_controller_builder
        self.merge_besu_controller_builder = merge_besu_controller_builder

    def prepForBuild(self) -> None:
        self.pre_merge_besu_controller_builder.prepForBuild()
        self.merge_besu_controller_builder.prepForBuild()

    def createMiningCoordinator(
        self,
        protocol_schedule: ProtocolSchedule,
        protocol_context: ProtocolContext,
        transaction_pool: TransactionPool,
        mining_parameters: MiningParameters,
        sync_state: SyncState,
        eth_protocol_manager: EthProtocolManager,
    ) -> MiningCoordinator:
        # Cast to TransitionProtocolSchedule for explicit access to pre and post objects
        transition_protocol_schedule = cast(
            TransitionProtocolSchedule, protocol_schedule
        )

        # Get consensus-specific mining parameters for TransitionCoordinator
        transition_mining_parameters = self.pre_merge_besu
