from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from magic_hour import MagicHourAPIError, MagicHourClient


class MagicHourProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            MagicHourClient(str(credentials.get("api_key", ""))).get_account()
        except MagicHourAPIError as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
