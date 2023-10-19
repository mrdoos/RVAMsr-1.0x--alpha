import os
import tempfile
import time
from typing import List, Optional
from urllib.parse import urlparse
from urllib.request import urlopen

import requests
from eth_utils import encode_hex
from requests.exceptions import ConnectionError
from requests.models import PreparedRequest
from requests.structures import CaseInsensitiveDict


class Enclave:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def up_check(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/upcheck")
            return response.status_code == 200
        except ConnectionError:
            return False

    def receive(self, key: str, public_key: str):
        try:
            response = requests.get(
                f"{self.base_url}/receive",
                headers={"Accept": "application/json"},
                params={"key": key, "publicKey": public_key},
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise Exception(f"Message with hash was not found: {e}")

    def send(self, payload: str, recipient: str, private_for: Optional[List[str]] = None):
        data = {"payload": payload, "to": recipient, "privateFor": private_for or []}
        response = requests.post(f"{self.base_url}/send", json=data)
        response.raise_for_status()
        return response.json()

    def create_privacy_group(
        self, addresses: List[str], from_address: str, name: str, description: str
    ):
        data = {
            "addresses": addresses,
            "from": from_address,
            "name": name,
            "description": description,
        }
        response = requests.post(f"{self.base_url}/createPrivacyGroup", json=data)
        response.raise_for_status()
        return response.json()

    def delete_privacy_group(self, privacy_group_id: str, from_address: str):
        response = requests.delete(
            f"{self.base_url}/privacyGroup/{privacy_group_id}", params={"from": from_address}
        )
        response.raise_for_status()
        return response.json()

    def find_privacy_group(self, addresses: List[str]):
        response = requests.get(
            f"{self.base_url}/findPrivacyGroup",
            headers={"Accept": "application/json"},
            params={"addresses": addresses},
        )
        response.raise_for_status()
        return response.json()

    def retrieve_privacy_group(self, privacy_group_id: str):
        response = requests.get(f"{self.base_url}/privacyGroup/{privacy_group_id}")
        response.raise_for_status()
        return response.json()


def test_up_check():
    enclave = Enclave("http://localhost:8080")
    assert enclave.up_check() is True


def test_receive_throws_when_payload_does_not_exist():
    enclave = Enclave("http://localhost:8080")
    mock_key = "iOCzoGo5kwtZU0J41Z9xnGXHN6ZNukIa9MspvHtu3Jk="
    public_key = "..."
    try:
        enclave.receive(mock_key, public_key)
    except Exception as e:
        assert str(e) == "Message with hash was not found"


def test_send_and_receive():
    enclave = Enclave("http://localhost:8080")
    payload = "a wonderful transaction"
    public_keys = ["..."]
    recipient = public_keys[0]

    send_response = enclave.send(payload, recipient, public_keys)
    key = send_response["key"]

    receive_response =
