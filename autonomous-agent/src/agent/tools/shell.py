import asyncio
from typing import Any

from src.agent.core.config import settings
from src.agent.tools.base import BaseTool, ToolResult


class SandboxedShellTool(BaseTool):
    name = "sandboxed_shell"
    description = "Executes a shell command in the sandbox directory."
    schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "The shell command to execute"}
        },
        "required": ["command"],
    }
    permission_level = "execute"
    risk_classification = "high"
    timeout_seconds = 120

    async def execute(self, **kwargs: Any) -> ToolResult:
        command = kwargs.get("command", "")
        sandbox_path = settings.SANDBOX_DIR

        process = await asyncio.create_subprocess_shell(
            command,
            cwd=sandbox_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=self.timeout_seconds
            )

            output = stdout.decode("utf-8")
            error = stderr.decode("utf-8")

            if process.returncode == 0:
                return ToolResult(output=output, success=True)
            else:
                return ToolResult(output=output, error=error, success=False)

        except asyncio.TimeoutError:
            process.kill()
            return ToolResult(
                output=None,
                error=f"Command timed out after {self.timeout_seconds} seconds",
                success=False,
            )

    async def verify(self, result: ToolResult, **kwargs: Any) -> bool:
        return result.success
