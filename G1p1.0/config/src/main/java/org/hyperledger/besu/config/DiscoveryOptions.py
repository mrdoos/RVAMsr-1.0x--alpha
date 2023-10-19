from typing import List, Optional
from typing_extensions import TypedDict

class DiscoveryOptions:
    class DiscoveryConfigRoot(TypedDict):
        bootnodes: Optional[List[str]]
        dns: Optional[str]

    def __init__(self, discoveryConfigRoot: DiscoveryConfigRoot):
        self.discoveryConfigRoot = discoveryConfigRoot

    def get_boot_nodes(self) -> Optional[List[str]]:
        boot_nodes = self.discoveryConfigRoot.get('bootnodes')
        if boot_nodes is None:
            return None
        return [str(node) for node in boot_nodes]

    def get_discovery_dns_url(self) -> Optional[str]:
        return self.discoveryConfigRoot.get('dns')
