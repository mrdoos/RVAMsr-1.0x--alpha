import logging

from .privacy_plugin_service import PrivacyPluginService
from .privacy_group_auth_provider import PrivacyGroupAuthProvider
from .privacy_group_genesis_provider import PrivacyGroupGenesisProvider
from .privacy_plugin_payload_provider import PrivacyPluginPayloadProvider
from .private_marker_transaction_factory import PrivateMarkerTransactionFactory

logger = logging.getLogger(__name__)


class PrivacyPluginServiceImpl(PrivacyPluginService):
    def __init__(self):
        self.privacy_plugin_payload_provider = None
        self.private_marker_transaction_factory = None
        self.privacy_group_auth_provider = lambda privacy_group_id, privacy_user_id, block_number: True
        self.privacy_group_genesis_provider = None

    def set_payload_provider(self, privacy_plugin_payload_provider: PrivacyPluginPayloadProvider) -> None:
        self.privacy_plugin_payload_provider = privacy_plugin_payload_provider

    def get_payload_provider(self) -> PrivacyPluginPayloadProvider:
        if self.privacy_plugin_payload_provider is None:
            logger.error("You must register a PrivacyPluginService and register a PrivacyPluginPayloadProvider "
                         "by calling set_payload_provider when enabling the privacy plugin!")
        return self.privacy_plugin_payload_provider

    def set_privacy
