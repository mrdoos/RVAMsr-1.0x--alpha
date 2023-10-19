from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore
from time import time

from besu.controller import BesuController
from besu.ethereum import BlockHeader
from besu.ethereum.block_importer import BlockImporter
from besu.ethereum.mainnet import BlockHeaderValidator, HeaderValidationMode
from besu.ethereum.protocol import ProtocolContext, ProtocolSchedule, ProtocolSpec
from besu.ethereum.util.raw_block_iterator import RawBlockIterator
from besu.ethereum.core import Block
from besu.ethereum.core import Transaction
from besu.ethereum.difficulty import Difficulty

import logging


class RlpBlockImporter:
    def __init__(self):
        self.blockBacklog = Semaphore(2)
        self.validationExecutor = ThreadPoolExecutor()
        self.importExecutor = ThreadPoolExecutor()
        self.cumulativeGas = 0
        self.segmentGas = 0
        self.cumulativeTimer = time()
        self.segmentTimer = time()
        self.SEGMENT_SIZE = 1000

    def close(self):
        self.validationExecutor.shutdown()
        self.importExecutor.shutdown()

    def importBlockchain(self, blocks, besuController, skipPowValidation, startBlock=0, endBlock=float("inf")):
        protocolSchedule = besuController.getProtocolSchedule()
        context = besuController.getProtocolContext()
        blockchain = context.getBlockchain()
        count = 0

        with RawBlockIterator(blocks, lambda rlp: BlockHeader.readFrom(rlp, ScheduleBasedBlockHeaderFunctions.create(protocolSchedule))) as iterator:
            previousHeader = None
            previousBlockFuture = None
            threadedException = None
            while iterator.hasNext():
                block = iterator.next()
                header = block.getHeader()
                blockNumber = header.getNumber()
                if blockNumber == BlockHeader.GENESIS_BLOCK_NUMBER or blockNumber < startBlock or blockNumber >= endBlock:
                    continue
                if blockchain.contains(header.getHash()):
                    continue
                if previousHeader is None:
                    previousHeader = self.lookupPreviousHeader(blockchain, header)
                protocolSpec = protocolSchedule.getByBlockNumber(blockNumber)
                lastHeader = previousHeader

                def validateBlock():
                    nonlocal threadedException
                    try:
                        blockHeaderValidator = protocolSpec.getBlockHeaderValidator()
                        validHeader = blockHeaderValidator.validateHeader(header, lastHeader, context, HeaderValidationMode.LIGHT_DETACHED_ONLY if skipPowValidation else HeaderValidationMode.DETACHED_ONLY)
                        if not validHeader:
                            raise Exception(f"Invalid header at block number {header.getNumber()}.")
                    except Exception as e:
                        threadedException = e

                def extractSignatures():s
                    for tx in block.getBody().getTransactions():
                        tx.getSender()

                def evaluateBlock():
                    nonlocal previousBlockFuture, threadedException
                    try:
                        self.cumulativeTimer = time()
                        self.segmentTimer = time()
                        blockImporter = protocolSpec.getBlockImporter()
                        blockImported = blockImporter.importBlock(context, block, HeaderValidationMode.LIGHT_SKIP_DETACHED if skipPowValidation else HeaderValidationMode.SKIP_DETACHED, HeaderValidationMode.LIGHT if skipPowValidation else HeaderValidationMode.FULL)
                        if not blockImported:
                            raise Exception(f"Invalid block at block number {header.getNumber()}.")
                    except Exception as e:
                        threadedException = e
                    finally:
                        self.blockBacklog.release()
                        self.cumulativeGas += block.getHeader().getGasUsed()
                        self.segmentGas += block.getHeader().getGasUsed()
                        if header.getNumber() % self.SEGMENT_SIZE == 0:
                            self.logProgress(blockchain.getChainHeadBlockNumber())

                validationFuture = self.validation
