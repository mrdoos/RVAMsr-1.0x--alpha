from web3 import Web3
from web3.contract import Contract

DEFAULT_GAS_PRICE = 1000
DEFAULT_GAS_LIMIT = 3000000
BENEFACTOR_ONE = Web3.toChecksumAddress("0xGENESIS_ACCOUNT_ONE_ADDRESS")

class DeploySmartContractTransaction:
    def __init__(self, clazz, *args):
        self.clazz = clazz
        self.args = args

    def execute(self, node):
        try:
            web3 = node.eth()
            if self.args:
                parameter_objects = [web3, BENEFACTOR_ONE, DEFAULT_GAS_PRICE, DEFAULT_GAS_LIMIT]
                parameter_objects.extend(self.args)

                deploy_method = next(
                    (
                        method
                        for method in self.clazz.__dict__.values()
                        if callable(method) and method.__name__ == "deploy"
                        and self.parameter_types_are_equal(method.__code__.co_varnames, parameter_objects)
                    ),
                    None
                )

                if deploy_method is None:
                    raise Exception("Matching deploy method not found.")

                deployed_contract = deploy_method(*parameter_objects)
                return deployed_contract.send()
            else:
                deploy_method = getattr(self.clazz, "deploy")
                deployed_contract = deploy_method(web3, BENEFACTOR_ONE, DEFAULT_GAS_PRICE, DEFAULT_GAS_LIMIT)
                return deployed_contract.send()
        except Exception as e:
            raise RuntimeError(str(e))

    def parameter_types_are_equal(self, expected_types, actual_objects):
        if len(expected_types) != len(actual_objects):
            return False

        actual_types = [type(obj) for obj in actual_objects]

        for expected_type, actual_type in zip(expected_types, actual_types):
            if not issubclass(actual_type, expected_type):
                return False

        return True