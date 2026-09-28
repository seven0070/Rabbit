import asyncio
from src.agent.research.observer import SubjectivityObserver

async def main():
    class MockDB:
        def add(self, obj): pass
        async def commit(self): pass

    observer = SubjectivityObserver(MockDB(), "test-identity-99")

    await observer.record_state(
        confidence=0.85,
        uncertainty=0.15,
        summary="Focused on writing files.",
        attention="Sandbox directory",
        measurements={"cpu_usage": 15, "memory_gb": 1.2}
    )

    import os
    print("Telemetry files:", os.listdir("telemetry"))

    with open("telemetry/subjectivity_test-identity-99.jsonl", "r") as f:
        print("Last line:", f.readlines()[-1].strip())

if __name__ == "__main__":
    asyncio.run(main())
