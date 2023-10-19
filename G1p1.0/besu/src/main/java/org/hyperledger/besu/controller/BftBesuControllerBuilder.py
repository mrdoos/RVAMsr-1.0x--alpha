/*
 * Copyright ConsenSys AG.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

from abc import ABC, abstractmethod
from functools import cached_property

from typing import Callable

class BftExtraDataCodec:
    def __init__(self):
        pass
    # Implement the BftExtraDataCodec methods here

class BftBlockInterface:
    def __init__(self, bft_extra_data_codec: BftExtraDataCodec):
        pass
    # Implement the BftBlockInterface methods here

class BftBesuControllerBuilder(ABC):
    @abstractmethod
    def bft_extra_data_codec(self) -> Callable[[], BftExtraDataCodec]:
        pass

    @cached_property
    def bft_block_interface(self) -> Callable[[], BftBlockInterface]:
        return lambda: BftBlockInterface(self.bft_extra_data_codec())

class BesuControllerBuilder:
    pass
    # Implement the BesuControllerBuilder methods here
