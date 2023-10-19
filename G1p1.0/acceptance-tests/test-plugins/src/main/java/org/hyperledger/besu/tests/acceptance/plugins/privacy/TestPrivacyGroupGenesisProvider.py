from typing import List, Dict
from dataclasses import dataclass
from eth_utils import to_canonical_address
from eth_typing import Address
from web3 import Web3
from web3.datastructures import AttributeDict
from web3.contract import Contract
from web3.types import Wei, UInt256


@dataclass
class PrivacyGenesisAccount:
    address: Address
    storage: Dict[UInt256, UInt256]
    nonce: int
    balance: Wei
    code: bytes


class TestPrivacyGroupGenesisProvider:
    def __init__(self):
        self.genesis_enabled = False

    def set_genesis_enabled(self):
        self.genesis_enabled = True

    def get_privacy_genesis(self, privacy_group_id: bytes, block_number: int):
        if not self.genesis_enabled:
            return []

        return [
            PrivacyGenesisAccount(
                address=to_canonical_address("0x1000000000000000000000000000000000000001"),
                storage={},
                nonce=0,
                balance=Wei(1000),
                code=bytes.fromhex(
                    "0x608060405260043610610057576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff1680633fa4f2451461005c5780636057361d1461008757806367e404ce146100c2575b600080fd5b34801561006857600080fd5b50610071610119565b6040518082815260200191505060405180910390f35b34801561009357600080fd5b506100c0600480360360208110156100aa57600080fd5b8101908080359060200190929190505050610123565b005b3480156100ce57600080fd5b506100d76101d9565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000600254905090565b7fc9db20adedc6cf2b5d25252b101ab03e124902a73fcb12b753f3d1aaa2d8f9f53382604051808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020018281526020019250505060405180910390a18060028190555033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b6000600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1690509056fea165627a7a72305820e74360c3d08936cb1747ad641729261ff5e83b6fc0d303d136e171f15f07d7740029",
                ),
            )
        ]
