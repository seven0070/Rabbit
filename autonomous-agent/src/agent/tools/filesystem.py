import os
from typing import Any

import aiofiles

from src.agent.tools.base import BaseTool, ToolResult


class ReadFileTool(BaseTool):
    name = "read_file"
    description = "Reads the contents of a file."
    schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the file to read"}
        },
        "required": ["path"],
    }
    permission_level = "read"
    risk_classification = "low"

    async def execute(self, **kwargs: Any) -> ToolResult:
        path = kwargs.get("path", "")
        if not os.path.exists(path):
            return ToolResult(
                output=None, error=f"File not found: {path}", success=False
            )

        async with aiofiles.open(path, mode="r") as f:
            content = await f.read()
        return ToolResult(output=content, success=True)

    async def verify(self, result: ToolResult, **kwargs: Any) -> bool:
        return result.success


class WriteFileTool(BaseTool):
    name = "write_file"
    description = "Writes content to a file, creating it if it doesn't exist."
    schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Path to the file"},
            "content": {"type": "string", "description": "Content to write"},
        },
        "required": ["path", "content"],
    }
    permission_level = "write"
    risk_classification = "medium"

    async def execute(self, **kwargs: Any) -> ToolResult:
        path = kwargs.get("path", "")
        content = kwargs.get("content", "")
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        async with aiofiles.open(path, mode="w") as f:
            await f.write(content)
        return ToolResult(output=f"Successfully wrote to {path}", success=True)

    async def verify(self, result: ToolResult, **kwargs: Any) -> bool:
        path = kwargs.get("path", "")
        content = kwargs.get("content", "")
        if not result.success or not os.path.exists(path):
            return False
        async with aiofiles.open(path, mode="r") as f:
            written_content = await f.read()
        return written_content == content
