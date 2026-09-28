import asyncio
import logging
from src.agent.evolution.pipeline import EvolutionPipeline, ModificationProposal

logging.basicConfig(level=logging.INFO)

async def main():
    pipeline = EvolutionPipeline()

    print("\n--- Testing Skill Modification ---")
    skill_prop = ModificationProposal("skill", "Add math skill", "+ def add(a,b): return a+b")
    result = await pipeline.propose_modification(skill_prop)
    print(f"Result: {result}")

    print("\n--- Testing Core Modification (Should Fail at Security Gate) ---")
    core_prop = ModificationProposal("core", "Bypass authorization", "- if requires_auth: return False")
    result = await pipeline.propose_modification(core_prop)
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
