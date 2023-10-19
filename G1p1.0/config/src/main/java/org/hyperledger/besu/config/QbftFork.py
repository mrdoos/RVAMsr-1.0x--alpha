class QbftFork(BftFork):
    class VALIDATOR_SELECTION_MODE(Enum):
        BLOCKHEADER = 1
        CONTRACT = 2

    VALIDATOR_SELECTION_MODE_KEY = "validatorselectionmode"
    VALIDATOR_CONTRACT_ADDRESS_KEY = "validatorcontractaddress"

    def __init__(self, forkConfigRoot):
        super().__init__(forkConfigRoot)

    def get_validator_selection_mode(self):
        mode = JsonUtil.get_string(self.forkConfigRoot, self.VALIDATOR_SELECTION_MODE_KEY)
        return next((v for v in self.VALIDATOR_SELECTION_MODE if v.name().equalsIgnoreCase(mode)), None)

    def get_validator_contract_address(self):
        return JsonUtil.get_string(self.forkConfigRoot, self.VALIDATOR_CONTRACT_ADDRESS_KEY)
