from typing import List
from dataclasses import dataclass

@dataclass
class BlockData:
    # Defina as propriedades do bloco aqui
    pass

@dataclass
class ChainData:
    blocks: List[BlockData]

    @classmethod
    def from_json(cls, json_data):
        blocks = [BlockData.from_json(block) for block in json_data.get("blocks", [])]
        return cls(blocks=blocks)
