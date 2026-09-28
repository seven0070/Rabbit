import asyncio
from src.agent.tools.filesystem import ReadFileTool, WriteFileTool
from src.agent.tools.shell import SandboxedShellTool

async def main():
    writer = WriteFileTool()
    reader = ReadFileTool()
    shell = SandboxedShellTool()

    write_res = await writer.run(path="sandbox/test.txt", content="hello world")
    print("Write:", write_res.success)

    read_res = await reader.run(path="sandbox/test.txt")
    print("Read:", read_res.output)

    shell_res = await shell.run(command="ls -la")
    print("Shell:", shell_res.output)

if __name__ == "__main__":
    asyncio.run(main())
