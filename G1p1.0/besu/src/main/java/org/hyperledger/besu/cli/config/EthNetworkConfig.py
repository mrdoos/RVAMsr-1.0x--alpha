import json
from typing import List, Optional
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class EnodeURL:
    node_id: str
    ip_address: str
    port: int


@dataclass
class GenesisConfigOptions:
    boot_nodes: List[str]
    discovery_dns_url: Optional[str]


@dataclass
class EthNetworkConfig:
    genesis_config: str
    network_id: int
    boot_nodes: List[EnodeURL]
    dns_discovery_url: Optional[str]


def json_config(resource_name: str) -> str:
    with open(resource_name, "r") as file:
        return file.read()


def get_network_config(network_name: str) -> EthNetworkConfig:
    genesis_content = json_config(network_name)
    genesis_config_options = json.loads(genesis_content)["config"]["genesis"]["config"]
    boot_nodes = []
    if "bootnodes" in genesis_config_options["discovery"]:
        boot_nodes = [
            EnodeURL(
                node_id=urlparse(boot_node).hostname,
                ip_address=urlparse(boot_node).hostname,
                port=urlparse(boot_node).port,
            )
            for boot_node in genesis_config_options["discovery"]["bootnodes"]
        ]
    dns_discovery_url = (
        genesis_config_options["discovery"]["discoveryDnsUrl"]
        if "discoveryDnsUrl" in genesis_config_options["discovery"]
        else None
    )
    return EthNetworkConfig(
        genesis_config=genesis_content,
        network_id=genesis_config_options["chainId"],
        boot_nodes=boot_nodes,
        dns_discovery_url=dns_discovery_url,
    )
