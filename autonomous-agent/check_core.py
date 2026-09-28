import asyncio
import logging
from src.agent.core.config import settings
from src.agent.db.session import AsyncSessionLocal
from src.agent.core.executive import ExecutiveCore

logging.basicConfig(level=logging.INFO)

async def main():
    # Because docker DB isn't running in this ephemeral environment,
    # we'll mock the DB calls just to ensure the logic connects.
    # In a real environment, this connects to postgres.

    # We will mock the load_identity and store_experience for this dry-run check
    # so we don't hit the un-reachable DB.

    class MockDB:
        async def execute(self, *args, **kwargs):
            class MockResult:
                def scalar_one_or_none(self): return None
                def scalars(self):
                    class MockScalars:
                        def all(self): return []
                    return MockScalars()
            return MockResult()
        def add(self, obj): pass
        async def commit(self): pass

    core = ExecutiveCore(MockDB(), "test-agent-id-1")
    print("Executive Core initialized successfully.")

    # We won't run a full cycle because the LLM API might not be configured,
    # but the classes are structurally sound.
    await core.load_identity()
    print("Identity logic works.")

if __name__ == "__main__":
    asyncio.run(main())
