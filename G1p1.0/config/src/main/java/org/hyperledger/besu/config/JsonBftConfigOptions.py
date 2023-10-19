import json
from typing import Optional
from eth_utils import to_checksum_address
from web3 import Web3

class JsonBftConfigOptions(BftConfigOptions):
    DEFAULT_EPOCH_LENGTH = 30_000
    DEFAULT_BLOCK_PERIOD_SECONDS = 1
    DEFAULT_ROUND_EXPIRY_SECONDS = 1
    DEFAULT_GOSSIPED_HISTORY_LIMIT = 1000
    DEFAULT_MESSAGE_QUEUE_LIMIT = 1000
    DEFAULT_DUPLICATE_MESSAGE_LIMIT = 100
    DEFAULT_FUTURE_MESSAGES_LIMIT = 1000
    DEFAULT_FUTURE_MESSAGES_MAX_DISTANCE = 10

    def __init__(self, bft_config_root):
        self.bft_config_root = bft_config_root

    def get_epoch_length(self):
        return self.bft_config_root.get("epochlength", self.DEFAULT_EPOCH_LENGTH)

    def get_block_period_seconds(self):
        return self.bft_config_root.get("blockperiodseconds", self.DEFAULT_BLOCK_PERIOD_SECONDS)

    def get_request_timeout_seconds(self):
        return self.bft_config_root.get("requesttimeoutseconds", self.DEFAULT_ROUND_EXPIRY_SECONDS)

    def get_gossiped_history_limit(self):
        return self.bft_config_root.get("gossipedhistorylimit", self.DEFAULT_GOSSIPED_HISTORY_LIMIT)

    def get_message_queue_limit(self):
        return self.bft_config_root.get("messagequeuelimit", self.DEFAULT_MESSAGE_QUEUE_LIMIT)

    def get_duplicate_message_limit(self):
        return self.bft_config_root.get("duplicatemessagelimit", self.DEFAULT_DUPLICATE_MESSAGE_LIMIT)

    def get_future_messages_limit(self):
        return self.bft_config_root.get("futuremessageslimit", self.DEFAULT_FUTURE_MESSAGES_LIMIT)

    def get_future_messages_max_distance(self):
        return self.bft_config_root.get("futuremessagesmaxdistance", self.DEFAULT_FUTURE_MESSAGES_MAX_DISTANCE)

    def get_mining_beneficiary(self) -> Optional[str]:
        mining_beneficiary = self.bft_config_root.get("miningbeneficiary")
        if mining_beneficiary:
            mining_beneficiary = mining_beneficiary.strip()
            if mining_beneficiary:
                try:
                    return to_checksum_address(mining_beneficiary)
                except ValueError:
                    raise ValueError("Mining beneficiary in config is not a valid Ethereum address")
        return None

    def get_block_reward_wei(self):
        block_reward = self.bft_config_root.get("blockreward")
        if block_reward:
            if block_reward.startswith("0x"):
                block_reward = block_reward[2:]
                return Web3.toInt(hexstr=block_reward)
            return int(block_reward)
        return 0

    def as_map(self):
        return {
            "epochLength": self.get_epoch_length(),
            "blockPeriodSeconds": self.get_block_period_seconds(),
            "requestTimeoutSeconds": self.get_request_timeout_seconds(),
            "gossipedHistoryLimit": self.get_gossiped_history_limit(),
            "messageQueueLimit": self.get_message_queue_limit(),
            "duplicateMessageLimit": self.get_duplicate_message_limit(),
            "futureMessagesLimit": self.get_future_messages_limit(),
            "futureMessagesMaxDistance": self.get_future_messages_max_distance()
        }
