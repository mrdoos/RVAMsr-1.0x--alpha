from typing import Callable, Dict, TypeVar, Collection
from itertools import compress

T = TypeVar('T')
PluginRpcRequest = TypeVar('PluginRpcRequest')

class RpcEndpointService:
    def __init__(self):
        self.rpcMethods: Dict[str, Callable[[PluginRpcRequest], T]] = {}

    def registerRPCEndpoint(
        self,
        namespace: str,
        functionName: str,
        function: Callable[[PluginRpcRequest], T]
    ) -> None:
        assert namespace.isalnum(), "Namespace must be only alphanumeric"
        assert functionName.isalnum(), "Function Name must be only alphanumeric"

        self.rpcMethods[namespace + "_" + functionName] = function

    def getPluginMethods(
        self,
        namespaces: Collection[str]
    ) -> Dict[str, Callable[[PluginRpcRequest], T]]:
        return {
            key: value
            for key, value in self.rpcMethods.items()
            if any(key.upper().startswith(namespace.upper()) for namespace in namespaces)
        }

    def hasNamespace(self, namespace: str) -> bool:
        return any(key.upper().startswith(namespace.upper()) for key in self.rpcMethods.keys())
