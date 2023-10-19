from typing import Callable
from functools import cached_property
from dataclasses import dataclass

@dataclass
class BftExtraDataCodec:
    # Implement BftExtraDataCodec methods here
    pass

@dataclass
class BftBlockInterface:
    bft_extra_data_codec: BftExtraDataCodec
    # Implement BftBlockInterface methods here
    pass

class BftBesuControllerBuilder:
    def bft_extra_data_codec(self) -> Callable[[], BftExtraDataCodec]:
        # Implement bft_extra_data_codec method here
        pass

    @cached_property
    def bft_block_interface(self) -> Callable[[], BftBlockInterface]:
        return lambda: BftBlockInterface(self.bft_extra_data_codec())

class BesuControllerBuilder:
    pass
    # Implement BesuControllerBuilder methods here
