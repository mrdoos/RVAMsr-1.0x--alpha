from besu.controller import PluginServiceFactory
from besu.consensus.common.bft import BftBlockInterface
from besu.consensus.common.bft.queries import BftQueryServiceImpl
from besu.consensus.common.validator import ValidatorProvider
from besu.consensus.ibft.queries import IbftQueryServiceImpl
from besu.crypto import NodeKey
from besu.ethereum.chain import Blockchain
from besu.plugin.services.metrics import PoAMetricsService
from besu.plugin.services.query import BftQueryService, IbftQueryService, PoaQueryService
from besu.services import BesuPluginContextImpl

class IbftQueryPluginServiceFactory(PluginServiceFactory):
    def __init__(self, blockchain, blockInterface, validatorProvider, nodeKey):
        self.blockchain = blockchain
        self.blockInterface = blockInterface
        self.validatorProvider = validatorProvider
        self.nodeKey = nodeKey

    def appendPluginServices(self, besuContext):
        service = IbftQueryServiceImpl(self.blockInterface, self.blockchain, self.nodeKey)
        besuContext.add_service(IbftQueryService, service)
        besuContext.add_service(PoaQueryService, service)
        besuContext.add_service(PoAMetricsService, service)

        bftService = BftQueryServiceImpl(self.blockInterface, self.blockchain, self.validatorProvider, self.nodeKey, "ibft")
        besuContext.add_service(BftQueryService, bftService)
