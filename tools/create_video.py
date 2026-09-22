from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from magic_hour import MagicHourClient


class CreateVideoTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        prompt = str(tool_parameters.get("prompt", "")).strip()
        if not prompt:
            raise ValueError("Prompt is required")

        payload: dict[str, Any] = {
            "end_seconds": float(tool_parameters.get("duration_seconds", 5)),
            "style": {"prompt": prompt},
        }
        for name in ("aspect_ratio", "resolution"):
            if value := tool_parameters.get(name):
                payload[name] = value
        model = str(tool_parameters.get("model", "")).strip()
        if model and model != "default":
            payload["model"] = model
        if tool_parameters.get("audio") is True:
            payload["audio"] = True

        result = MagicHourClient(self.runtime.credentials["api_key"]).create_text_to_video(payload)
        yield self.create_variable_message("result", result)
