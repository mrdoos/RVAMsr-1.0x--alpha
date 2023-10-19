from typing import Optional, List
from dataclasses import dataclass
from eth_utils import from_hex, to_int, to_bytes, to_checksum_address, to_bytes32
from eth_keys import keys
from eth_typing import Address, Hash
from eth_utils import decode_hex, big_endian_to_int
from eth_utils import keccak
from eth_utils.hexadecimal import encode_hex

@dataclass
class TransactionData:
    # Define as propriedades da transação aqui
    pass

@dataclass
class BlockData:
    number: Optional[int]
    parentHash: Optional[Hash]
    transactionData: List[TransactionData]
    coinbase: Optional[Address]
    extraData: Optional[bytes]

    @classmethod
    def from_json(cls, json_data):
        number = to_int(from_hex(json_data.get("number", "")))
        parent_hash = Hash(decode_hex(json_data.get("parentHash", "")))
        coinbase = to_checksum_address(json_data.get("coinbase", ""))
        extra_data = to_bytes(json_data.get("extraData", ""))
        transactions = json_data.get("transactions", [])
        transaction_data = [TransactionData.from_json(tx) for tx in transactions]

        return cls(number=number, parentHash=parent_hash, coinbase=coinbase,
                   extraData=extra_data, transactionData=transaction_data)
