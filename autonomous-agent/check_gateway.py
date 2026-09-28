import asyncio
from src.agent.llm.gateway import ModelGateway

async def main():
    gateway = ModelGateway()
    print("Available providers:", list(gateway.providers.keys()))

if __name__ == "__main__":
    asyncio.run(main())
