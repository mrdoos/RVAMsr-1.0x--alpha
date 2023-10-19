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
package org.hyperledger.besu.config;

import java.util.Map;

import com.fasterxml.jackson.databind.node.ObjectNode;import json
from typing import Dict
from web3 import Web3

class IbftLegacyConfigOptions:
    DEFAULT_EPOCH_LENGTH = 30_000
    DEFAULT_BLOCK_PERIOD_SECONDS = 1
    DEFAULT_ROUND_EXPIRY_SECONDS = 1
    DEFAULT_CEIL_2N_BY_3_BLOCK = 0

    def __init__(self, ibft_config_root):
        self.ibft_config_root = ibft_config_root

    def get_epoch_length(self):
        return self.ibft_config_root.get("epochlength", self.DEFAULT_EPOCH_LENGTH)

    def get_block_period_seconds(self):
        return self.ibft_config_root.get("blockperiodseconds", self.DEFAULT_BLOCK_PERIOD_SECONDS)

    def get_request_timeout_seconds(self):
        return self.ibft_config_root.get("requesttimeoutseconds", self.DEFAULT_ROUND_EXPIRY_SECONDS)

    def get_ceil2nby3_block(self):
        return self.ibft_config_root.get("ceil2nby3block", self.DEFAULT_CEIL_2N_BY_3_BLOCK)

    def as_map(self) -> Dict[str, object]:
        return {
            "epochLength": self.get_epoch_length(),
            "blockPeriodSeconds": self.get_block_period_seconds(),
            "requestTimeoutSeconds": self.get_request_timeout_seconds(),
            "ceil2nby3block": self.get_ceil2nby3_block()
        }

import com.google.common.collect.ImmutableMap;

public class IbftLegacyConfigOptions {

  public static final IbftLegacyConfigOptions DEFAULT =
      new IbftLegacyConfigOptions(JsonUtil.createEmptyObjectNode());

  private static final long DEFAULT_EPOCH_LENGTH = 30_000;
  private static final int DEFAULT_BLOCK_PERIOD_SECONDS = 1;
  private static final int DEFAULT_ROUND_EXPIRY_SECONDS = 1;
  private static final long DEFAULT_CEIL_2N_BY_3_BLOCK = 0L;

  private final ObjectNode ibftConfigRoot;

  IbftLegacyConfigOptions(final ObjectNode ibftConfigRoot) {
    this.ibftConfigRoot = ibftConfigRoot;
  }

  public long getEpochLength() {
    return JsonUtil.getLong(ibftConfigRoot, "epochlength", DEFAULT_EPOCH_LENGTH);
  }

  public int getBlockPeriodSeconds() {
    return JsonUtil.getPositiveInt(
        ibftConfigRoot, "blockperiodseconds", DEFAULT_BLOCK_PERIOD_SECONDS);
  }

  public int getRequestTimeoutSeconds() {
    return JsonUtil.getInt(ibftConfigRoot, "requesttimeoutseconds", DEFAULT_ROUND_EXPIRY_SECONDS);
  }

  public long getCeil2Nby3Block() {
    return JsonUtil.getLong(ibftConfigRoot, "ceil2nby3block", DEFAULT_CEIL_2N_BY_3_BLOCK);
  }

  Map<String, Object> asMap() {
    final ImmutableMap.Builder<String, Object> builder = ImmutableMap.builder();
    if (ibftConfigRoot.has("epochlength")) {
      builder.put("epochLength", getEpochLength());
    }
    if (ibftConfigRoot.has("blockperiodseconds")) {
      builder.put("blockPeriodSeconds", getBlockPeriodSeconds());
    }
    if (ibftConfigRoot.has("requesttimeoutseconds")) {
      builder.put("requestTimeoutSeconds", getRequestTimeoutSeconds());
    }
    if (ibftConfigRoot.has("ceil2nby3block")) {
      builder.put("ceil2nby3block", getCeil2Nby3Block());
    }

    return builder.build();
  }
}
