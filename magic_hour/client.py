from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx
from dify_plugin.file.file import File


class MagicHourAPIError(RuntimeError):
    pass


class MagicHourClient:
    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise MagicHourAPIError("Magic Hour API key is required")
        self._client = httpx.Client(
            base_url="https://api.magichour.ai",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60,
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = self._client.request(method, endpoint, **kwargs)
        except httpx.HTTPError as exc:
            raise MagicHourAPIError(f"Magic Hour request failed: {exc}") from exc

        if response.is_error:
            try:
                detail = response.json().get("message", response.text)
            except ValueError:
                detail = response.text
            raise MagicHourAPIError(f"Magic Hour API returned {response.status_code}: {detail}")

        try:
            return response.json()
        except ValueError as exc:
            raise MagicHourAPIError("Magic Hour returned an invalid JSON response") from exc

    def get_account(self) -> dict[str, Any]:
        return self._request("GET", "/v1/account")

    def create_image(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/ai-image-generator", json=payload)

    def create_image_to_video(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/image-to-video", json=payload)

    def create_text_to_video(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/text-to-video", json=payload)

    def get_image_project(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/image-projects/{project_id}")

    def get_video_project(self, project_id: str) -> dict[str, Any]:
        return self._request("GET", f"/v1/video-projects/{project_id}")

    def upload_image(self, image: File) -> str:
        extension = (image.extension or Path(image.filename or "").suffix).lower().lstrip(".")
        if not extension and image.mime_type:
            extension = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}.get(image.mime_type, "")
        allowed = {"avif", "bmp", "gif", "heic", "heif", "jfif", "jp2", "jpeg", "jpg", "png", "tif", "tiff", "webp"}
        if extension not in allowed:
            raise MagicHourAPIError("Input must be a supported image file")

        upload = self._request(
            "POST",
            "/v1/files/upload-urls",
            json={"items": [{"type": "image", "extension": extension}]},
        )["items"][0]

        try:
            response = httpx.put(upload["upload_url"], content=image.blob, timeout=120)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise MagicHourAPIError(f"Image upload failed: {exc}") from exc
        return upload["file_path"]
