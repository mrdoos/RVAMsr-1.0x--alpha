imimport unittest
from besu_tests.acceptance.dsl.account import Account
from besu_tests.acceptance.dsl.node import BesuNode
from besu_tests.acceptance.bft.pki.parameterized_pki_qbft_test_base import ParameterizedPkiQbftTestBase

class PkiQbftAcceptanceTest(ParameterizedPkiQbftTestBase):
    def __init__(self, testName, input):
        super().__init__(testName, input)

    def test_should_mine_on_single_node(self):
        minerNode = nodeFactory.createNode(besu, "miner1")
        cluster.start(minerNode)

        cluster.verify(blockchain.reachesHeight(minerNode, 1))

        sender = accounts.createAccount("account1")
        receiver = accounts.createAccount("account2")

        minerNode.execute(accountTransactions.createTransfer(sender, 50))
        cluster.verify(sender.balanceEquals(50))

        minerNode.execute(accountTransactions.createIncrementalTransfers(sender, receiver, 1))
        cluster.verify(receiver.balanceEquals(1))

        minerNode.execute(accountTransactions.createIncrementalTransfers(sender, receiver, 2))
        cluster.verify(receiver.balanceEquals(3))

    def test_should_mine_on_multiple_nodes(self):
        minerNode1 = nodeFactory.createNode(besu, "miner1")
        minerNode2 = nodeFactory.createNode(besu, "
