from enum import Enum
from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class NetworkInfo:
    genesis_file: str
    network_id: int
    can_fast_sync: bool


class NetworkName(Enum):
    MAINNET = NetworkInfo("/mainnet.json", 1, True)
    RINKEBY = NetworkInfo("/rinkeby.json", 4, True)
    ROPSTEN = NetworkInfo("/ropsten.json", 3, True)
    SEPOLIA = NetworkInfo("/sepolia.json", 11155111, True)
    GOERLI = NetworkInfo("/goerli.json", 5, True)
    KILN = NetworkInfo("/kiln.json", 1337802, False)
    DEV = NetworkInfo("/dev.json", 2018, False)
    CLASSIC = NetworkInfo("/classic.json", 1, True)
    KOTTI = NetworkInfo("/kotti.json", 6, True)
    MORDOR = NetworkInfo("/mordor.json", 7, True)
    ECIP1049_DEV = NetworkInfo("/ecip1049_dev.json", 2021, True)
    ASTOR = NetworkInfo("/astor.json", 212, True)

    def get_genesis_file(self) -> str:
        return self.value.genesis_file

    def get_network_id(self) -> int:
        return self.value.network_id

    def can_fast_sync(self) -> bool:
        return self.value.can_fast_sync
