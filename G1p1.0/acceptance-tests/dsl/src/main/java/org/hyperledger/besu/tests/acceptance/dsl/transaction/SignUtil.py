from web3 import Web3
from web3._utils.transactions import encode_transaction, TRANSACTION_DEFAULTS
from web3._utils.signing import sign_transaction_dict
from web3.eth import Eth

class SignUtil:
    @staticmethod
    def sign_transaction(
        transaction, sender, signature_algorithm, chain_id=None
    ):
        encoded_transaction = encode_transaction(
            transaction, vrs=TRANSACTION_DEFAULTS["vrs"], chain_id=chain_id
        )

        credentials = sender.web3j_credentials_or_throw()
        private_key = signature_algorithm.create_private_key(
            credentials.ec_key_pair.private_key
        )

        transaction_hash = Web3.keccak(encoded_transaction)

        signature = signature_algorithm.sign(
            transaction_hash, signature_algorithm.create_key_pair(private_key)
        )

        signed_transaction = sign_transaction_dict(
            encoded_transaction, signature, signature_algorithm
        )

        return signed_transaction