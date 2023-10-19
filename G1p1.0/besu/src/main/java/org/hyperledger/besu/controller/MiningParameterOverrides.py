from besu.ethereum.core import MiningParameters


class MiningParameterOverrides:
    def get_mining_parameter_overrides(self, from_cli: MiningParameters) -> MiningParameters:
        return from_cli
