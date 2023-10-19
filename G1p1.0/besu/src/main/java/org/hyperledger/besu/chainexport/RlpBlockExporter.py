import os
import logging
from eth_typing import BlockNumber
from eth_utils import to_checksum_address
from eth_keys import keys
from eth_keys.exceptions import ValidationError
from eth_utils.hexadecimal import decode_hex
from eth_utils.encoding import to_bytes
from eth_utils import keccak

logger = logging.getLogger(__name__)

class RlpBlockExporter(BlockExporter):
    def __init__(self, blockchain):
        super().__init__(blockchain)

    def export_block(self, file, block):
        rlp_data = block.to_rlp_bytes()
        file.write(rlp_data)
