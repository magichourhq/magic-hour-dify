from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from magic_hour import MagicHourClient


class GetImageProjectTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        project_id = str(tool_parameters.get("project_id", "")).strip()
        if not project_id:
            raise ValueError("Project ID is required")

        project = MagicHourClient(self.runtime.credentials["api_key"]).get_image_project(project_id)
        yield self.create_variable_message("result", project)
        if project.get("status") == "complete":
            for download in project.get("downloads", []):
                if url := download.get("url"):
                    yield self.create_image_message(url)
