from typing import Optional, List
from eth_typing import Address
from decimal import Decimal
from typing import Dict

class BftFork:
    FORK_BLOCK_KEY = "block"
    VALIDATORS_KEY = "validators"
    BLOCK_PERIOD_SECONDS_KEY = "blockperiodseconds"
    BLOCK_REWARD_KEY = "blockreward"
    MINING_BENEFICIARY_KEY = "miningbeneficiary"

    def __init__(self, forkConfigRoot: Dict):
        self.forkConfigRoot = forkConfigRoot

    def get_fork_block(self) -> int:
        fork_block = self.forkConfigRoot.get(self.FORK_BLOCK_KEY)
        if fork_block is None:
            raise ValueError("Fork block not specified for Bft fork in custom forks")
        return fork_block

    def get_block_period_seconds(self) -> Optional[int]:
        return self.forkConfigRoot.get(self.BLOCK_PERIOD_SECONDS_KEY)

    def get_block_reward_wei(self) -> Optional[Decimal]:
        block_reward = self.forkConfigRoot.get(self.BLOCK_REWARD_KEY)
        if block_reward is None:
            return None
        if block_reward.lower().startswith("0x"):
            return Decimal(int(block_reward, 16))
        return Decimal(block_reward)

    def get_mining_beneficiary(self) -> Optional[Address]:
        mining_beneficiary = self.forkConfigRoot.get(self.MINING_BENEFICIARY_KEY)
        if mining_beneficiary:
            return Address(mining_beneficiary.strip())
        return None

    def is_mining_beneficiary_configured(self) -> bool:
        return self.MINING_BENEFICIARY_KEY in self.forkConfigRoot

    def get_validators(self) -> Optional[List[str]]:
        validators = self.forkConfigRoot.get(self.VALIDATORS_KEY)
        if validators is None:
            return None
        return [str(validator) for validator in validators]
