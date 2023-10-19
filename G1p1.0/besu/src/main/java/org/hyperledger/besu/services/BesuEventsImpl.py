from typing import List
from functools import partial
from abc import ABC, abstractmethod
from datetime import datetime
from random import randrange

class BesuEvents(ABC):
    @abstractmethod
    def addBlockPropagatedListener(self, listener) -> int:
        pass

    @abstractmethod
    def removeBlockPropagatedListener(self, listenerIdentifier: int) -> None:
        pass

    @abstractmethod
    def addBlockAddedListener(self, listener) -> int:
        pass

    @abstractmethod
    def removeBlockAddedListener(self, listenerIdentifier: int) -> None:
        pass

    @abstractmethod
    def addBlockReorgListener(self, listener) -> int:
        pass

    @abstractmethod
    def removeBlockReorgListener(self, listenerIdentifier: int) -> None:
        pass

    @abstractmethod
    def addTransactionAddedListener(self, listener) -> int:
        pass

    @abstractmethod
    def removeTransactionAddedListener(self, listenerIdentifier: int) -> None:
        pass

    @abstractmethod
    def addTransactionDroppedListener(self, listener) -> int:
        pass

    @abstractmethod
    def removeTransactionDroppedListener(self, listenerIdentifier: int) -> None:
        pass

    @abstractmethod
    def addSyncStatusListener(self, listener) -> int:
        pass

    @abstractmethod
    def removeSyncStatusListener(self, listenerIdentifier: int) -> None:
        pass

    @abstractmethod
    def addLogListener(
        self, addresses: List[str], topics: List[List[str]], listener
    ) -> int:
        pass

    @abstractmethod
    def removeLogListener(self, listenerIdentifier: int) -> None:
        pass


class BesuEventsImpl(BesuEvents):
    def __init__(self):
        self.listener_identifiers = {}

    def addBlockPropagatedListener(self, listener) -> int:
        listener_identifier = randrange(1, 1000)  # Generate a random identifier
        self.listener_identifiers[listener_identifier] = listener
        return listener_identifier

    def removeBlockPropagatedListener(self, listenerIdentifier: int) -> None:
        if listenerIdentifier in self.listener_identifiers:
            del self.listener_identifiers[listenerIdentifier]

    def addBlockAddedListener(self, listener) -> int:
        listener_identifier = randrange(1, 1000)  # Generate a random identifier
        self.listener_identifiers[listener_identifier] = listener
        return listener_identifier

    def removeBlockAddedListener(self, listenerIdentifier: int) -> None:
        if listenerIdentifier in self.listener_identifiers:
            del self.listener_identifiers[listenerIdentifier]

    def addBlockReorgListener(self, listener) -> int:
        listener_identifier = randrange(1, 1000)  # Generate a random identifier
        self.listener_identifiers[listener_identifier] = listener
        return listener_identifier

    def removeBlockReorgListener(self, listenerIdentifier: int) -> None:
        if listenerIdentifier in self.listener_identifiers:
            del self.listener_identifiers[listenerIdentifier]

    def addTransactionAddedListener(self, listener) -> int:
        listener_identifier = randrange(1, 1000)  # Generate a random identifier
        self.listener_identifiers[listener_identifier] = listener
        return listener_identifier

    def removeTransactionAddedListener(self, listenerIdentifier: int) -> None:
        if listenerIdentifier in self.listener_identifiers:
            del self.listener_identifiers[listenerIdentifier
