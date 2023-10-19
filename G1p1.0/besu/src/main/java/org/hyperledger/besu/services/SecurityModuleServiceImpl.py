from typing import Callable, Dict, Optional, Supplier

class SecurityModuleService:
    def __init__(self):
        self.securityModuleSuppliers: Dict[str, Supplier[SecurityModule]] = {}

    def register(
        self,
        name: str,
        securityModuleSupplier: Supplier[SecurityModule]
    ) -> None:
        self.securityModuleSuppliers[name] = securityModuleSupplier

    def getByName(self, name: str) -> Optional[Supplier[SecurityModule]]:
        return self.securityModuleSuppliers.get(name)


class SecurityModule:
    pass
