import logging

from eth_keys import keys
from eth_utils import keccak
from eth_typing import Address

from eth_account.transaction import (
    Transaction,
    UnsignedTransaction,
    FrontierTransaction,
    TypeOneTransaction,
)
from eth_account.datastructures import (
    PrivateTransaction,
    UnsignedPrivateMarkerTransaction,
)
from eth_account.messages import encode_rlp_payload

logger = logging.getLogger(__name__)


class TestSigningPrivateMarkerTransactionFactory:
    def __init__(self):
        self.alice_fixed_signing_key = None
        self.sender = None

    def set_signing_key_enabled(self, private_marker_transaction_signing_key):
        signature_algorithm = keys.SignatureAlgorithm(secp256k1=True)
        private_key = keys.PrivateKey(bytes.fromhex(private_marker_transaction_signing_key))

        self.alice_fixed_signing_key = keys.PrivateKey(private_key)
        self.sender = self.extract_address(self.alice_fixed_signing_key)

    def create(
        self,
        unsigned_private_marker_transaction: UnsignedPrivateMarkerTransaction,
        private_transaction: PrivateTransaction,
        privacy_user_id: str,
    ):
        transaction = Transaction(
            nonce=unsigned_private_marker_transaction.nonce,
            gas_price=(
                Wei(unsigned_private_marker_transaction.gas_price)
                if unsigned_private_marker_transaction.gas_price is not None
                else None
            ),
            gas=unsigned_private_marker_transaction.gas_limit,
            to=(
                Address(unsigned_private_marker_transaction.to)
                if unsigned_private_marker_transaction.to is not None
                else None
            ),
            value=Wei(unsigned_private_marker_transaction.value),
            data=unsigned_private_marker_transaction.payload,
        )

        if private_transaction:
            payload = encode_rlp_payload(private_transaction.to_dict())
            transaction.type = TypeOneTransaction(payload=payload)

        logger.info("Signing PMT from {}".format(self.sender))

        signed_transaction = transaction.as_signed_transaction(
            self.alice_fixed_signing_key
        )

        return signed_transaction.encode()

    def get_sender(self, private_transaction: PrivateTransaction, privacy_user_id: str):
        return self.sender

    @staticmethod
    def extract_address(key):
        public_key = key.public_key
        address_bytes = keccak(public_key.to_bytes()[1:])[-20:]
        return Address(address_bytes)
