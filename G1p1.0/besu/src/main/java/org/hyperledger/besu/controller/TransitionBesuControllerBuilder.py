from typing import Optional
from functools import partial
from itertools import chain

from eth_keys import keys
from eth_typing import NodeID
from eth_utils import decode_hex, encode_hex
from py_ecc import bn128
from web3 import Web3

from besu.bft import BftConfigOptions, BftProtocolManager, Istanbul100SubProtocol
from besu.common import MainnetChainIdProvider
from besu.ethereum.chain import ChainConfig, ChainContext, ChainContextFactory
from besu.ethereum.eth import EthProtocol
from besu.ethereum.eth.config import EthProtocolConfiguration
from besu.ethereum.eth.validators import EthValidator
from besu.ethereum.mainnet import (MainnetConsensusContext,
                                   MainnetProtocolSchedule)
from besu.ethereum.mainnet.genesis_state import (GenesisConfig, GenesisState,
                                                 create_genesis_config)
from besu.ethereum.mainnet.mainnet_constants import (
    FRONTIER_BLOCK_NUMBER,
    BYZANTIUM_BLOCK_NUMBER,
    ISTANBUL_BLOCK_NUMBER,
)
from besu.ethereum.mainnet.mining import (create_mainnet_proof_of_work_validator,
                                          create_minimal_difficulty_validator)
from besu.ethereum.mainnet.pow import (FrontierDifficultyCalculator,
                                       DifficultyCalculatorAPI,
                                       FrontierDifficultyApplier,
                                       FrontierProofOfWorkValidator,
                                       ByzantiumProofOfWorkValidator,
                                       ConstantinopleProofOfWorkValidator,
                                       IstanbulProofOfWorkValidator)
from besu.ethereum.mainnet.pow.ethash import create_epoch_calculator
from besu.ethereum.mainnet.vm_configuration import (IstanbulVMConfiguration,
                                                    MainnetVMConfiguration,
                                                    MainnetChainConfig)
from besu.ethereum.pow.ethash import EthashParams
from besu.ethereum.world_state import WorldStateArchive
from besu.ethereum.world_state.merkle_patricia_world_state import (
    BLANK_ROOT_HASH,
    MerklePatriciaWorldState,
)
from besu.ethereum.world_state.state_archive import StateArchive
from besu.ethereum.world_state.state_archive_writer import StateArchiveWriter
from besu.p2p.config import P2PConfig
from besu.p2p.discovery import NodeDiscoveryService
from besu.p2p.discovery.enr import Enr
from besu.p2p.discovery.upnp import UPnPService
from besu.p2p.kademlia import KademliaRoutingTable
from besu.p2p.network import (DiscoveryConfig,
                              SimpleAddressBook,
                              SimpleNetwork,
                              UPnPService,
                              connect_to_bootstrap_nodes)
from besu.plugins import BaseBesuPlugin
from besu.plugins.bootnode_plugin import BootnodePlugin
from besu.plugins.core import AdminPlugin, DebugPlugin, MetricsPlugin
from besu.plugins.ethash_plugin import EthashPlugin
from besu.plugins.json_rpc_plugin import JSONRPCPlugin
from besu.plugins.mining import MiningPlugin
from besu.plugins.perf_plugin import PerfPlugin
from besu.plugins.permissioning import PermissioningPlugin
from besu.plugins.websocket_plugin import WebsocketPlugin
from besu.util import get_open_port
from besu.validators import MainnetValidators


def create_node_key() -> keys.PrivateKey:
    return keys.PrivateKey(bn128.scalar_random())


def create_genesis_state(
    config: GenesisConfig, chain_id: int
) -> GenesisState:
    # Ethereum genesis states are created using the Ethereum
    # initialize_genesis_state API
    #
    # `initial_allocations` is a dictionary with addresses as keys and
    # allocation amounts as values.
    # Example:
    # initial_alloc
