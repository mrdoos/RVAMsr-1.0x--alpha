import json
import urllib.parse
import urllib.request

from org.hyperledger.besu.enclave import RequestTransmitter, EnclaveClientException, EnclaveServerException
from org.hyperledger.besu.enclave.types import (
    GoQuorumReceiveResponse,
    GoQuorumSendRequest,
    GoQuorumSendSignedRequest,
    GoQuorumStoreRawRequest,
    SendResponse,
    StoreRawResponse,
)


class GoQuorumEnclave:
    JSON = "application/json"

    def __init__(self, request_transmitter):
        self.request_transmitter = request_transmitter

    def up_check(self):
        try:
            upcheck_response = self.request_transmitter.get(None, None, "/upcheck", self.handle_raw_response, False)
            return upcheck_response == "I'm up!"
        except Exception:
            return False

    def send(self, payload, private_from, private_for):
        request = GoQuorumSendRequest(payload, private_from, private_for)
        return self.post(
            GoQuorumEnclave.JSON,
            request,
            "/send",
            lambda status_code, body: self.handle_json_response(status_code, body, SendResponse, 201),
        )

    def send_signed_transaction(self, tx_lookup_id, private_for):
        request = GoQuorumSendSignedRequest(tx_lookup_id, private_for)
        return self.post(
            GoQuorumEnclave.JSON,
            request,
            "/sendsignedtx",
            lambda status_code, body: self.handle_json_response(status_code, body, SendResponse, 201),
        )

    def store_raw(self, payload):
        request = GoQuorumStoreRawRequest(payload)
        return self.post(
            GoQuorumEnclave.JSON,
            request,
            "/storeraw",
            lambda status_code, body: self.handle_json_response(status_code, body, StoreRawResponse, 200),
        )

    def receive(self, payload_key):
        encoded_payload_key = urllib.parse.quote(payload_key)
        return self.get(
            GoQuorumEnclave.JSON,
            f"/transaction/{encoded_payload_key}",
            lambda status_code, body: self.handle_json_response(status_code, body, GoQuorumReceiveResponse, 200),
        )

    def post(self, media_type, content, endpoint, response_body_handler):
        try:
            body_text = json.dumps(content)
        except json.JSONDecodeError:
            raise EnclaveClientException(400, "Unable to serialize request.")
        return self.request_transmitter.post(media_type, body_text, endpoint, response_body_handler)

    def get(self, media_type, endpoint, response_body_handler):
        return self.request_transmitter.get(media_type, None, endpoint, response_body_handler, True)

    def handle_json_response(self, status_code, body, response_type, expected_status_code):
        if self.is_success(status_code, expected_status_code):
            return self.parse_response(status_code, body, response_type)
        elif self.client_error(status_code):
            raise EnclaveClientException(status_code, body.decode("utf-8"))
        else:
            raise EnclaveServerException(status_code, body.decode("utf-8"))

    def parse_response(self, status_code, body, response_type):
        try:
            return json.loads(body.decode("utf-8"), object_hook=response_type)
        except json.JSONDecodeError:
            raise EnclaveClientException(status_code, body.decode("utf-8"))

    def client_error(self, status_code):
        return 400 <= status_code < 500

    def is_success(self, status_code, expected_status_code):
        return status_code == expected_status_code

    def handle_raw
