import logging

from besu.controller import BesuControllerBuilder
from besu.consensus.common import BlockInterface, EpochManager, ValidatorProvider
from besu.consensus.ibft import IbftLegacyBlockInterface, IbftProtocolSchedule, IbftLegacyContext
from besu.ethereum.mainnet import ProtocolSchedule
from besu.ethereum.p2p import SubProtocolConfiguration
from besu.ethereum.worldstate import WorldStateArchive
from besu.services.mining import MiningCoordinator, NoopMiningCoordinator
from besu.services.transaction_pool import TransactionPool

LOG = logging.getLogger(__name__)

class IbftLegacyBesuControllerBuilder(BesuControllerBuilder):
    def __init__(self):
        self.blockInterface = IbftLegacyBlockInterface()

    def createSubProtocolConfiguration(self, ethProtocolManager, snapProtocolManager):
        return SubProtocolConfiguration().with_sub_protocol(Istanbul99Protocol.get(), ethProtocolManager)

    def createMiningCoordinator(self, protocolSchedule, protocolContext, transactionPool, miningParameters, syncState, ethProtocolManager):
        return NoopMiningCoordinator(miningParameters)

    def createProtocolSchedule(self):
        return IbftProtocolSchedule.create(configOptionsSupplier.get(), privacyParameters, isRevertReasonEnabled, evmConfiguration)

    def createConsensusContext(self, blockchain, worldStateArchive, protocolSchedule):
        ibftConfig = configOptionsSupplier.get().getIbftLegacyConfigOptions()
        epochManager = EpochManager(ibftConfig.getEpochLength())
        validatorProvider = BlockValidatorProvider.non_forking_validator_provider(blockchain, epochManager, self.blockInterface)

        return IbftLegacyContext(validatorProvider, epochManager, self.blockInterface)

    def createAdditionalPluginServices(self, blockchain, protocolContext):
        return NoopPluginServiceFactory()

    def validateContext(self, context):
        genesisBlockHeader = context.blockchain.get_genesis_block().header

        if self.blockInterface.validators_in_block(genesisBlockHeader):
            LOG.warn("Genesis block contains no signers - chain will not progress.")

    def get_supported_protocol(self):
        return Istanbul99Protocol.get().get_name()

    def create_eth_protocol_manager(self, protocolContext, fastSyncEnabled, transactionPool, ethereumWireProtocolConfiguration, ethPeers, ethContext, ethMessages, scheduler, peerValidators):
        LOG.info("Operating on IBFT-1.0 network.")
        return Istanbul99ProtocolManager(protocolContext.blockchain, networkId, protocolContext.world_state_archive, transactionPool, ethereumWireProtocolConfiguration, ethPeers, ethMessages, ethContext, peerValidators, fastSyncEnabled, scheduler)
