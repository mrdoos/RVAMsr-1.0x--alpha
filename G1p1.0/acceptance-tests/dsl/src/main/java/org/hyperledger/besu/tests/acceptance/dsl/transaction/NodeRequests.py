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
from web3 import Web3

class NodeRequests:
    def __init__(
        self,
        net_eth,
        clique,
        bft,
        perm,
        admin,
        privacy,
        custom,
        miner,
        tx_pool,
        websocket_service,
        login,
    ):
        self.net_eth = net_eth
        self.clique = clique
        self.bft = bft
        self.perm = perm
        self.admin = admin
        self.privacy = privacy
        self.custom = custom
        self.miner = miner
        self.tx_pool = tx_pool
        self.websocket_service = websocket_service
        self.login = login

    def eth(self):
        return self.net_eth

    def net(self):
        return self.net_eth

    def clique(self):
        return self.clique

    def bft(self):
        return self.bft

    def perm(self):
        return self.perm

    def admin(self):
        return self.admin

    def custom(self):
        return self.custom

    def privacy(self):
        return self.privacy

    def login(self):
        return self.login

    def miner(self):
        return self.miner

    def tx_pool(self):
        return self.tx_pool

    def shutdown(self):
        self.net_eth.shutdown()
        if self.websocket_service:
            self.websocket_service.close()