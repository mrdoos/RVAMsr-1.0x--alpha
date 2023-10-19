import json
from typing import Optional, List
from eth_utils import to_checksum_address
from web3 import Web3

class BlockData:
    def __init__(self, parent_hash: Optional[str], number: Optional[int], coinbase: Optional[str], extra_data: Optional[str]):
        self.parent_hash = parent_hash
        self.number = number
        self.coinbase = coinbase
        self.extra_data = extra_data

class ChainData:
    def __init__(self, blocks: List[BlockData]):
        self.blocks = blocks

class JsonBlockImporter:
    def __init__(self, controller):
        self.controller = controller

    def import_chain(self, chain_json: str):
        self.warn_if_database_is_not_empty()

        chain_data = json.loads(chain_json, object_hook=self.json_to_chain_data)
        imported_blocks = []
        for block_data in chain_data.blocks:
            parent_header = self.get_parent_header(block_data, imported_blocks)
            imported_block = self.process_block_data(block_data, parent_header)
            imported_blocks.append(imported_block)

        self.warn_if_imported_blocks_are_not_on_canonical_chain(imported_blocks)

    def process_block_data(self, block_data, parent_header):
        print("Preparing to import block at height {} (parent: {})".format(parent_header.number + 1, parent_header.hash))

        world_state = self.controller.get_protocol_context().get_world_state_archive().get(parent_header.state_root, parent_header.hash)
        transactions = block_data.stream_transactions(world_state)
        transactions_list = list(transactions)

        block = self.create_block(block_data, parent_header, transactions_list)
        self.assert_all_transactions_included(block, transactions_list)
        self.import_block(block)

        return block

    def create_block(self, block_data, parent_header, transactions):
        miner = self.controller.get_mining_coordinator()
        genesis_config_options = self.controller.get_genesis_config_options()
        self.set_optional_fields(miner, block_data, genesis_config_options)

        return miner.create_block(parent_header, transactions, [])

    def set_optional_fields(self, miner, block_data, genesis_config):
        if genesis_config.pow_algorithm != PowAlgorithm.UNSUPPORTED:
            miner.set_coinbase(block_data.coinbase or "0x0000000000000000000000000000000000000000")
            miner.set_extra_data(block_data.extra_data or b'')
        elif block_data.coinbase or block_data.extra_data:
            raise ValueError("Some fields are unsupported by the current consensus engine: {}".format(genesis_config.consensus_engine))

    def import_block(self, block):
        importer = self.controller.get_protocol_schedule().get_by_block_number(block.header.number).get_block_importer()

        imported = importer.import_block(self.controller.get_protocol_context(), block, HeaderValidationMode.NONE)
        if imported:
            print("Successfully created and imported block at height {} ({})".format(block.header.number, block.hash))
        else:
            raise ValueError("Newly created block {} failed validation.".format(block.header.number))

    def assert_all_transactions_included(self, block, transactions):
        if len(transactions) != len(block.body.transactions):
            missing_transactions = len(transactions) - len(block.body.transactions)
            raise ValueError("Unable to create block. {} transaction(s) were found to be invalid.".format(missing_transactions))

    def warn_if_database_is_not_empty(self):
        chain_height = self.controller.get_protocol_context().get_blockchain().get_chain_head().height
        if chain_height > BlockHeader.GENESIS_BLOCK_NUMBER:
            print("Importing to a non-empty database with chain height {}. This may cause imported blocks to be considered non-can
