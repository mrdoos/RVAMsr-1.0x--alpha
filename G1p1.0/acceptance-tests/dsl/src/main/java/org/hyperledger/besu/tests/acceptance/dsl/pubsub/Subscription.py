from typing import Dict, List
from dataclasses import dataclass
from time import sleep
import re


@dataclass
class SubscriptionEvent:
    version: str
    method: str
    params: Dict[str, str]


class Subscription:
    SIXTY_FOUR_HEX_PATTERN = r"0x[0-9a-f]{64}"
    HEX_PATTERN = r"0x[0-9a-f]+"

    def __init__(self, connection, value):
        assert re.match(self.HEX_PATTERN, value), "Invalid value"
        self.value = value
        self.connection = connection

    def __str__(self):
        return self.value

    def verify_event_received(self, expected_transaction, expected_occurrences=1):
        for _ in range(10):  # Retry for a maximum of 10 times
            events = self.connection.get_subscription_events()
            occurrences = sum(
                self.matches(expected_transaction, event) for event in events
            )
            if occurrences == expected_occurrences:
                return  # Expected occurrences found, exit the loop
            sleep(1)  # Wait for 1 second before retrying
        assert False, f"Expected: {expected_occurrences} occurrences, but found: {occurrences}"

    def matches(self, expected_transaction, event):
        return (
            self.is_eth_subscription(event)
            and self.is_expected_subscription(event)
            and self.is_expected_transaction(expected_transaction, event)
        )

    @staticmethod
    def is_eth_subscription(event):
        return (
            event.version == "2.0"
            and event.method == "eth_subscription"
            and event.params is not None
        )

    def is_expected_subscription(self, event):
        params = event.params
        return (
            len(params) == 2
            and "subscription" in params
            and self.value == params["subscription"]
        )

    @staticmethod
    def is_expected_transaction(expected_transaction, event):
        params = event.params
        result = params.get("result")
        return (
            "result" in params
            and expected_transaction == result
            and re.match(Subscription.SIXTY_FOUR_HEX_PATTERN, result)
        )
