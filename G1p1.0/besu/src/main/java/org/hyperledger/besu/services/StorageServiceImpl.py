from typing import List, Optional
from enum import Enum
from collections import defaultdict


class KeyValueSegmentIdentifier(Enum):
    # Define your KeyValueSegmentIdentifier values here
    pass


class KeyValueStorageFactory:
    def __init__(self, name):
        self.name = name


class StorageService:
    def registerKeyValueStorage(self, factory: KeyValueStorageFactory):
        pass

    def getAllSegmentIdentifiers(self) -> List[KeyValueSegmentIdentifier]:
        pass

    def getByName(self, name: str) -> Optional[KeyValueStorageFactory]:
        pass


class StorageServiceImpl(StorageService):
    def __init__(self):
        self.segments = list(KeyValueSegmentIdentifier)
        self.factories = defaultdict(KeyValueStorageFactory)

    def registerKeyValueStorage(self, factory: KeyValueStorageFactory):
        self.factories[factory.name] = factory

    def getAllSegmentIdentifiers(self) -> List[KeyValueSegmentIdentifier]:
        return self.segments

    def getByName(self, name: str) -> Optional[KeyValueStorageFactory]:
        return self.factories.get(name)


# Example usage
storage_service = StorageServiceImpl()
factory = KeyValueStorageFactory("ExampleFactory")
storage_service.registerKeyValueStorage(factory)

all_segment_identifiers = storage_service.getAllSegmentIdentifiers()
for segment_identifier in all_segment_identifiers:
    print(segment_identifier)

factory_name = "ExampleFactory"
factory_optional = storage_service.getByName(factory_name)
if factory_optional is not None:
    print(factory_optional.name)
