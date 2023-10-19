from dataclasses import dataclass
from typing import Optional
from eth_keys import keys
from eth_typing import Address
from eth_utils import to_checksum_address
from eth_utils.hexadecimal import decode_hex
from eth_utils.hexadecimal import encode_hex
from eth_utils.hexadecimal import pad_hex
from eth_utils.hexadecimal import remove_0x_prefix
from eth_utils.hexadecimal import add_0x_prefix
from eth_utils.hexadecimal import is_hex
from eth_utils.hexadecimal import is_hex_address
from eth_utils.hexadecimal import is_prefixed_hex
from eth_utils.hexadecimal import is_same_address
from eth_utils.hexadecimal import is_valid_hex
from eth_utils.hexadecimal import is_zero_address
from eth_utils.hexadecimal import strip_hex_prefix
from eth_utils.hexadecimal import to_hex
from eth_utils.hexadecimal import to_hex_address
from eth_utils.hexadecimal import to_normalized_address
from eth_utils.hexadecimal import to_canonical_address
from eth_utils.hexadecimal import to_bytes
from eth_utils.hexadecimal import to_int
from eth_utils.hexadecimal import to_text
from eth_utils.hexadecimal import unpad_hex
from eth_utils.hexadecimal import hexstr_if_str
from eth_utils.hexadecimal import hexstr_if_bytes
from eth_utils.hexadecimal import hexstr_if_text
from eth_utils.hexadecimal import is_bytes
from eth_utils.hexadecimal import is_text
from eth_utils.hexadecimal import is_string
from eth_utils.hexadecimal import is_integer
from eth_utils.hexadecimal import is_integer_hex
from eth_utils.hexadecimal import remove_0x_prefix_if_hex
from eth_utils.hexadecimal import remove_0x_prefix_if_prefixed
from eth_utils.hexadecimal import add_0x_prefix_if_not_prefixed
from eth_utils.hexadecimal import add_0x_prefix_if_prefixed
from eth_utils.hexadecimal import is_same_address
from eth_utils.hexadecimal import is_zero_address
from eth_utils.hexadecimal import pad_hex
from eth_utils.hexadecimal import unpad_hex
from eth_utils.hexadecimal import decode_hex
from eth_utils.hexadecimal import encode_hex
from eth_utils.hexadecimal import to_hex
from eth_utils.hexadecimal import remove_0x_prefix

@dataclass
class TransactionData:
    gasLimit: int
    gasPrice: str
    data: bytes
    value: str
    to: Optional[str]
    privateKey: keys.PrivateKey

    def getSignedTransaction(self, nonceProvider):
        keyPair = keys.PrivateKey(self.privateKey.to_bytes())
        fromAddress = to_checksum_address(keyPair.public_key.to_canonical_address())
        nonce = nonceProvider.get(fromAddress)
        transaction = {
            'gasLimit': self.gasLimit,
            'gasPrice': self.gasPrice,
            'nonce': nonce,
            'data': self.data.hex(),
            'value': self.value,
            'to': self.to,
        }
        signed_tx = keyPair.sign_transaction(transaction)
        return signed_tx
