from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum


@dataclass
class IbftLegacyConfigOptions:
    # Add fields here as needed
    pass


@dataclass
class CliqueConfigOptions:
    # Add fields here as needed
    pass


@dataclass
class BftConfigOptions:
    # Add fields here as needed
    pass


@dataclass
class QbftConfigOptions:
    # Add fields here as needed
    pass


@dataclass
class DiscoveryOptions:
    # Add fields here as needed
    pass


@dataclass
class EthashConfigOptions:
    # Add fields here as needed
    pass


@dataclass
class Keccak256ConfigOptions:
    # Add fields here as needed
    pass


class PowAlgorithm(Enum):
    ETHASH = "ethash"
    KECCAK256 = "keccak256"


@dataclass
class TransitionsConfigOptions:
    # Add fields here as needed
    pass


@dataclass
class GenesisConfigOptions:
    def isEthHash(self) -> bool:
        pass

    def isKeccak256(self) -> bool:
        pass

    def isIbftLegacy(self) -> bool:
        pass

    def isIbft2(self) -> bool:
        pass

    def isQbft(self) -> bool:
        pass

    def isClique(self) -> bool:
        pass

    def isConsensusMigration(self) -> bool:
        pass

    def getConsensusEngine(self) -> str:
        pass

    def getIbftLegacyConfigOptions(self) -> IbftLegacyConfigOptions:
        pass

    def getCliqueConfigOptions(self) -> CliqueConfigOptions:
        pass

    def getBftConfigOptions(self) -> BftConfigOptions:
        pass

    def getQbftConfigOptions(self) -> QbftConfigOptions:
        pass

    def getDiscoveryOptions(self) -> DiscoveryOptions:
        pass

    def getEthashConfigOptions(self) -> EthashConfigOptions:
        pass

    def getKeccak256ConfigOptions(self) -> Keccak256ConfigOptions:
        pass

    def getHomesteadBlockNumber(self) -> Optional[int]:
        pass

    def getDaoForkBlock(self) -> Optional[int]:
        pass

    def getTangerineWhistleBlockNumber(self) -> Optional[int]:
        pass

    def getSpuriousDragonBlockNumber(self) -> Optional[int]:
        pass

    def getByzantiumBlockNumber(self) -> Optional[int]:
        pass

    def getConstantinopleBlockNumber(self) -> Optional[int]:
        pass

    def getPetersburgBlockNumber(self) -> Optional[int]:
        pass

    def getIstanbulBlockNumber(self) -> Optional[int]:
        pass

    def getMuirGlacierBlockNumber(self) -> Optional[int]:
        pass

    def getBerlinBlockNumber(self) -> Optional[int]:
        pass

    def getLondonBlockNumber(self) -> Optional[int]:
        pass

    def getArrowGlacierBlockNumber(self) -> Optional[int]:
        pass

    def getParisBlockNumber(self) -> Optional[int]:
        pass

    def getBaseFeePerGas(self) -> Optional[int]:
        pass

    def getTerminalTotalDifficulty(self) -> Optional[int]:
        pass

    def getTerminalBlockNumber(self) -> Optional[int]:
        pass

    def getTerminalBlockHash(self) -> Optional[str]:
        pass

    def getForks(self) -> List[int
