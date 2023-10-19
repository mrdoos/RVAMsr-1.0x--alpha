from typing import Dict, List, Optional
import json

class GenesisAllocation:
    def __init__(self, address: str, data: Dict[str, str]):
        self.address = address
        self.data = data

    def get_address(self) -> str:
        return self.address

    def get_balance(self) -> str:
        return self.data.get("balance", "0")

    def get_code(self) -> Optional[str]:
        return self.data.get("code")

    def get_nonce(self) -> str:
        return self.data.get("nonce", "0")

    def get_version(self) -> Optional[str]:
        return self.data.get("version")

    def get_storage(self) -> Dict[str, str]:
        return self.data.get("storage", {})


class GenesisConfigFile:
    DEFAULT = None
    BASEFEE_AT_GENESIS_DEFAULT_VALUE = 1000000000

    def __init__(self, config: Dict):
        self.configRoot = config

    @staticmethod
    def mainnet() -> 'GenesisConfigFile':
        return GenesisConfigFile.genesis_file_from_resources("/mainnet.json")

    @staticmethod
    def mainnet_json_node() -> Dict:
        with open('/path/to/mainnet.json', 'r') as file:
            return json.load(file)

    @staticmethod
    def development() -> 'GenesisConfigFile':
        return GenesisConfigFile.genesis_file_from_resources("/dev.json")

    @staticmethod
    def ecip1049dev() -> 'GenesisConfigFile':
        return GenesisConfigFile.genesis_file_from_resources("/ecip1049_dev.json")

    @staticmethod
    def genesis_file_from_resources(resource_name: str) -> 'GenesisConfigFile':
        with open(resource_name, 'r') as file:
            return GenesisConfigFile.from_config(file.read())

    @staticmethod
    def from_config(json_string: str) -> 'GenesisConfigFile':
        return GenesisConfigFile.from_config(json.loads(json_string))

    @staticmethod
    def from_config(config: Dict) -> 'GenesisConfigFile':
        return GenesisConfigFile(config)

    def get_config_options(self, overrides: Dict[str, str
