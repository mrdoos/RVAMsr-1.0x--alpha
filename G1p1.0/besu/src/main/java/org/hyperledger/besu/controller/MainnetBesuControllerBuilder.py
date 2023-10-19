ffrom besu.controller import BesuControllerBuilder, PluginServiceFactory
from besu.ethereum import ConsensusContext, ProtocolContext
from besu.ethereum.blockcreation import DefaultBlockScheduler, MiningCoordinator, PoWMinerExecutor, PoWMiningCoordinator
from besu.ethereum.chain import Blockchain
from besu.ethereum.core import MiningParameters
from besu.ethereum.eth.manager import EthProtocolManager
from besu.ethereum.eth.sync.state import SyncState
from besu.ethereum.eth.transactions import TransactionPool
from besu.ethereum.mainnet import EpochCalculator, MainnetBlockHeaderValidator, MainnetProtocolSchedule
from besu.ethereum.worldstate import WorldStateArchive


class MainnetBesuControllerBuilder(BesuControllerBuilder):
    def __init__(self):
        self.epochCalculator = EpochCalculator.DefaultEpochCalculator()

    def create_mining_coordinator(
        self,
        protocolSchedule,
        protocolContext,
        transactionPool,
        miningParameters,
        syncState,
        ethProtocolManager
    ):
        executor = PoWMinerExecutor(
            protocolContext,
            protocolSchedule,
            transactionPool.get_pending_transactions(),
            miningParameters,
            DefaultBlockScheduler(
                MainnetBlockHeaderValidator.MINIMUM_SECONDS_SINCE_PARENT,
                MainnetBlockHeaderValidator.TIMESTAMP_TOLERANCE_S,
                clock
            ),
            self.epochCalculator,
            miningParameters.getPowJobTimeToLive(),
            miningParameters.getMaxOmmerDepth()
        )

        miningCoordinator = PoWMiningCoordinator(
            protocolContext.getBlockchain(),
            executor,
            syncState,
            miningParameters.getRemoteSealersLimit(),
            miningParameters.getRemoteSealersTimeToLive()
        )
        miningCoordinator.add_mined_block_observer(ethProtocolManager)
        miningCoordinator.set_stratum_mining_enabled(miningParameters.isStratumMiningEnabled())
        if miningParameters.isMiningEnabled():
            miningCoordinator.enable()

        return miningCoordinator

    def create_consensus_context(self, blockchain, worldStateArchive, protocolSchedule):
        return None

    def create_additional_plugin_services(self, blockchain, protocolContext):
        return NoopPluginServiceFactory()

    def create_protocol_schedule(self):
        return MainnetProtocolSchedule.from_config(
            configOptionsSupplier.get(),
            privacyParameters,
            isRevertReasonEnabled,
            evmConfiguration
        )

    def prep_for_build(self):
        activationBlock = configOptionsSupplier.get().getThanosBlockNumber()
        if activationBlock is not None:
            self.epochCalculator = EpochCalculator.Ecip1099EpochCalculator()


class NoopPluginServiceFactory(PluginServiceFactory):
    def append_plugin_services(self, besuContext):
        pass
