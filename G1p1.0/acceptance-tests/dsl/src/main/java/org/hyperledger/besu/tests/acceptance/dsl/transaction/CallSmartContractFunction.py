from web3 import Web3
from eth_account import Account
from web3.exceptions import TransactionNotFound

class CallSmartContractFunction:
    GAS_PRICE = 1000
    GAS_LIMIT = 3000000
    BENEFACTOR_ONE_PRIVATE_KEY = "..."  # Chave privada da conta benefactor

    def __init__(self, function_name, contract_address):
        self.function_name = function_name
        self.contract_address = contract_address

    def execute(self, node):
        w3 = Web3(node.eth())  # Instanciar o objeto Web3 com o provedor Ethereum

        function = {
            "name": self.function_name,
            "inputs": [],
            "outputs": []
        }

        benefactor_one = Account.from_key(self.BENEFACTOR_ONE_PRIVATE_KEY)
        transaction_data = {
            "to": self.contract_address,
            "data": w3.eth.contract(abi=[], address=self.contract_address).encodeABI(fn_name=self.function_name),
            "gas": self.GAS_LIMIT,
            "gasPrice": self.GAS_PRICE,
            "nonce": w3.eth.getTransactionCount(benefactor_one.address),
            "value": 0
        }

        signed_tx = benefactor_one.signTransaction(transaction_data)
        try:
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            return tx_receipt
        except TransactionNotFound:
            raise ValueError("Transaction failed or not found.")