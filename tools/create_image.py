from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from magic_hour import MagicHourClient


class CreateImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        prompt = str(tool_parameters.get("prompt", "")).strip()
        if not prompt:
            raise ValueError("Prompt is required")

        payload: dict[str, Any] = {
            "image_count": int(tool_parameters.get("image_count", 1)),
            "style": {"prompt": prompt},
        }
        for name in ("aspect_ratio", "resolution"):
            if value := tool_parameters.get(name):
                payload[name] = value
        model = str(tool_parameters.get("model", "")).strip()
        if model and model != "default":
            payload["model"] = model

        result = MagicHourClient(self.runtime.credentials["api_key"]).create_image(payload)
        yield self.create_variable_message("result", result)
