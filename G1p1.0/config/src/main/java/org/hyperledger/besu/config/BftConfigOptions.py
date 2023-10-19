from typing import Optional
from dataclasses import dataclass
from decimal import Decimal
from eth_typing import Address
from typing import Dict

@dataclass
class BftConfigOptions:
    epoch_length: int
    block_period_seconds: int
    request_timeout_seconds: int
    gossiped_history_limit: int
    message_queue_limit: int
    duplicate_message_limit: int
    future_messages_limit: int
    future_messages_max_distance: int
    mining_beneficiary: Optional[Address]
    block_reward_wei: Decimal
    config_map: Dict[str, object]

    def as_map(self):
        return {
            "epochLength": self.epoch_length,
            "blockPeriodSeconds": self.block_period_seconds,
            "requestTimeoutSeconds": self.request_timeout_seconds,
            "gossipedHistoryLimit": self.gossiped_history_limit,
            "messageQueueLimit": self.message_queue_limit,
            "duplicateMessageLimit": self.duplicate_message_limit,
            "futureMessagesLimit": self.future_messages_limit,
            "futureMessagesMaxDistance": self.future_messages_max_distance,
            "miningBeneficiary": self.mining_beneficiary,
            "blockRewardWei": self.block_reward_wei,
            **self.config_map,
        }
