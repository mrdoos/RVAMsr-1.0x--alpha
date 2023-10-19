from besu.controller import BesuControllerBuilder, PluginServiceFactory
from besu.consensus.merge import MergeContext, MergeProtocolSchedule, PostMergeContext
from besu.consensus.merge.blockcreation import MergeCoordinator
from besu.datatypes import Hash
from besu.ethereum import ProtocolContext
from besu.ethereum.blockcreation import MiningCoordinator
from besu.ethereum.chain import Blockchain
from besu.ethereum.core import BlockHeader, Difficulty, MiningParameters
from besu.ethereum.eth.manager import EthProtocolManager
from besu.ethereum.eth.peervalidation import PeerValidator, RequiredBlocksPeerValidator
from besu.ethereum.eth.sync.backwardsync import BackwardChain, BackwardSyncContext
from besu.ethereum.eth.sync.state import SyncState
from besu.ethereum.eth.transactions import TransactionPool
from besu.ethereum.mainnet import ProtocolSchedule, ScheduleBasedBlockHeaderFunctions
from besu.ethereum.worldstate import WorldStateArchive
from concurrent.atomic import AtomicReference
import logging


class MergeBesuControllerBuilder(BesuControllerBuilder):
    def __init__(self):
        self.syncState = AtomicReference()
        self.LOG = logging.getLogger(MergeBesuControllerBuilder.__class__.__name__)

    def create_mining_coordinator(
        self,
        protocolSchedule,
        protocolContext,
        transactionPool,
        miningParameters,
        syncState,
        ethProtocolManager
    ):
        return self.create_transition_mining_coordinator(
            protocolSchedule,
            protocolContext,
            transactionPool,
            miningParameters,
            syncState,
            ethProtocolManager,
            BackwardSyncContext(
                protocolContext,
                protocolSchedule,
                metricsSystem,
                ethProtocolManager.ethContext(),
                syncState,
                BackwardChain.from(
                    storageProvider,
                    ScheduleBasedBlockHeaderFunctions.create(protocolSchedule)
                )
            )
        )

    def create_transition_mining_coordinator(
        self,
        protocolSchedule,
        protocolContext,
        transactionPool,
        miningParameters,
        syncState,
        ethProtocolManager,
        backwardSyncContext
    ):
        self.syncState.set(syncState)
        return MergeCoordinator(
            protocolContext,
            protocolSchedule,
            transactionPool.get_pending_transactions(),
            miningParameters,
            backwardSyncContext
        )

    def create_protocol_schedule(self):
        return MergeProtocolSchedule.create(
            configOptionsSupplier.get(),
            privacyParameters,
            isRevertReasonEnabled
        )

    def create_consensus_context(self, blockchain, worldStateArchive, protocolSchedule):
        terminalBlockNumber = configOptionsSupplier.get().getTerminalBlockNumber()
        terminalBlockHash = configOptionsSupplier.get().getTerminalBlockHash()

        mergeContext = (
            PostMergeContext.get()
            .set_sync_state(self.syncState.get())
            .set_terminal_total_difficulty(
                configOptionsSupplier.get().get_terminal_total_difficulty().map(Difficulty.of).orElse(Difficulty.ZERO)
            )
        )

        if terminalBlockNumber and terminalBlockHash:
            termBlock = blockchain.get_block_header(terminalBlockNumber)
            mergeContext.set_terminal_pow_block(termBlock)

        blockchain.get_finalized_block_header().if_present(mergeContext.set_finalized)
        blockchain.get_safe_block_header().if_present(mergeContext.set_safe_block)

        def on_block_added(blockAddedEvent):
            block_hash = blockAddedEvent.get_block().get_header().get_hash()
            blockchain.get_total_difficulty_by_hash(block_hash).if_present(mergeContext.set_is_post_merge)

        blockchain.observe_block_added(on_block_added)

        return mergeContext

    def create_additional_plugin_services(self, blockchain, protocolContext):
        return NoopPluginService
