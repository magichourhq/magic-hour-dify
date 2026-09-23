from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

from magic_hour import MagicHourClient


class AnimateImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        image = tool_parameters.get("image")
        if not isinstance(image, File):
            raise ValueError("An input image is required")

        client = MagicHourClient(self.runtime.credentials["api_key"])
        file_path = client.upload_image(image)
        payload: dict[str, Any] = {
            "end_seconds": float(tool_parameters.get("duration_seconds", 5)),
            "assets": {"image_file_path": file_path},
        }
        prompt = str(tool_parameters.get("prompt", "")).strip()
        if prompt:
            payload["style"] = {"prompt": prompt}
        model = str(tool_parameters.get("model", "")).strip()
        if model and model != "default":
            payload["model"] = model
        if resolution := tool_parameters.get("resolution"):
            payload["resolution"] = resolution
        if tool_parameters.get("audio") is True:
            payload["audio"] = True

        result = client.create_image_to_video(payload)
        yield self.create_variable_message("result", result)
