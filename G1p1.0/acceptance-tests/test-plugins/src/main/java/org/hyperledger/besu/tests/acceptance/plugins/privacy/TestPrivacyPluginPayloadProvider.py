from typing import Optional
from eth_utils import to_bytes, to_hex
from eth_keys import keys
from eth_typing import Address, HexStr
from web3.datastructures import AttributeDict
from web3 import Web3
from web3.contract import Contract

class TestPrivacyPluginPayloadProvider:
    def __init__(self):
        self.prefix = ""

    def set_plugin_payload_prefix(self, prefix: str):
        self.prefix = prefix

    def generate_marker_payload(
        self, private_transaction: AttributeDict, privacy_user_id: str
    ) -> bytes:
        prefix_bytes = to_bytes(hexstr=self.prefix)
        private_transaction_bytes = Web3.keccak(private_transaction)
        return prefix_bytes + private_transaction_bytes

    def get_private_transaction_from_payload(
        self, transaction: AttributeDict
    ) -> Optional[AttributeDict]:
        prefix_bytes = to_bytes(hexstr=self.prefix)
        if transaction["payload"].startswith(prefix_bytes):
            private_transaction_bytes = to_bytes(hexstr=transaction["payload"][len(prefix_bytes):])
            return AttributeDict(Web3.rlp.decode(private_transaction_bytes))
        else:
            return None
