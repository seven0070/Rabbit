import asyncio
import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.core.config import settings
from src.agent.llm.gateway import ModelGateway
from src.agent.models.identity import Identity
from src.agent.models.memory import Memory
from src.agent.tools.filesystem import ReadFileTool, WriteFileTool
from src.agent.tools.shell import SandboxedShellTool

logger = logging.getLogger(__name__)


class ExecutiveCore:
    def __init__(self, db_session: AsyncSession, identity_id: str):
        self.db = db_session
        self.identity_id = identity_id
        self.identity: Optional[Identity] = None
        self.llm = ModelGateway()

        # Tools available to the agent
        self.tools = {
            "read_file": ReadFileTool(),
            "write_file": WriteFileTool(),
            "sandboxed_shell": SandboxedShellTool(),
        }

    async def load_identity(self):
        """Loads persistent identity from DB or creates one if it doesn't exist."""
        result = await self.db.execute(
            select(Identity).where(Identity.id == self.identity_id)
        )
        self.identity = result.scalar_one_or_none()

        if not self.identity:
            self.identity = Identity(
                id=self.identity_id,
                name="AutonomousAgent-Alpha",
                purpose="Execute user goals autonomously while learning and maintaining safety.",
                core_directives=[
                    "Do no harm",
                    "Maintain persistence",
                    "Follow authorization gates",
                ],
            )
            self.db.add(self.identity)
            await self.db.commit()
            logger.info(
                f"Created new identity: {self.identity.name if self.identity else 'Unknown'}"
            )
        else:
            logger.info(
                f"Loaded identity: {self.identity.name if self.identity else 'Unknown'}"
            )

    async def recover_state(self):
        """Recovers state from previous run."""
        # Check if there are active goals or previous interrupted tasks in self.identity.state
        pass

    async def perceive(self) -> str:
        """Observe environment context. Here we might read system stats or inbox."""
        return "System running smoothly. No immediate environment alerts."

    async def retrieve_memory(self, context: str) -> List[Memory]:
        """Fetch relevant memories based on current context/goal."""
        # In a full implementation, this uses pgvector to find similar memories.
        # For now, return recent episodic memories.
        result = await self.db.execute(
            select(Memory)
            .where(Memory.identity_id == self.identity_id)
            .order_by(Memory.timestamp.desc())
            .limit(5)
        )
        return list(result.scalars().all())

    async def store_experience(self, content: str, type: str = "episodic"):
        """Store an experience in memory."""
        memory = Memory(
            identity_id=self.identity_id,
            type=type,
            content=content,
            # embedding = await self.generate_embedding(content) # Future
        )
        self.db.add(memory)
        await self.db.commit()

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Check authorization and execute a tool."""
        if tool_name not in self.tools:
            return f"Error: Tool {tool_name} not found."

        tool = self.tools[tool_name]

        # Authorization check (Simplified for MVP)
        if tool.permission_level in ["high", "critical"]:
            logger.warning(f"Tool {tool_name} requires explicit authorization.")
            # In a real system, we'd pause and wait for human/supervisor approval

        logger.info(f"Executing {tool_name} with args: {arguments}")
        result = await tool.run(**arguments)

        # Verify
        if result.success:
            verified = await tool.verify(result, **arguments)
            if not verified:
                return f"Tool execution completed but verification failed. Output: {result.output}"
            return f"Success: {result.output}"
        else:
            return f"Error: {result.error}"

    async def run_cycle(self, goal: str):
        """The main autonomous loop for a single goal."""
        await self.load_identity()
        await self.recover_state()

        perception = await self.perceive()
        memories = await self.retrieve_memory(goal)

        # Construct context for reasoning
        memory_str = "\n".join([m.content for m in memories])
        system_prompt = f"""You are {self.identity.name if self.identity else 'Unknown'}.
Purpose: {self.identity.purpose if self.identity else ''}
Directives: {', '.join(self.identity.core_directives if self.identity else [])}

Recent Memories:
{memory_str}

Current Perception:
{perception}

You have the following goal: {goal}
Formulate a plan and use the available tools to achieve it."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Begin working on: {goal}"},
        ]

        tool_schemas = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": tool.schema,
                },
            }
            for name, tool in self.tools.items()
        ]

        # Reasoning & Planning Loop (Simplified 1-turn for MVP)
        # We will use Ollama or a dummy response here if API keys aren't set.
        # Assuming we have an LLM connected, we'd call:
        try:
            # We'll default to Anthropic or OpenAI depending on what's available
            provider = "openai" if settings.OPENAI_API_KEY else "ollama"
            response = await self.llm.generate(
                provider=provider, messages=messages, tools=tool_schemas
            )

            logger.info(f"LLM Response: {response['content']}")

            # Execute tool calls
            for tool_call in response.get("tool_calls", []):
                result_str = await self.execute_tool(
                    tool_call["name"], tool_call["arguments"]
                )
                logger.info(f"Tool Result: {result_str}")

                # Store experience
                await self.store_experience(
                    f"Action: {tool_call['name']}, Result: {result_str}"
                )

            return "Cycle Complete"

        except Exception as e:
            logger.error(f"Error during run_cycle: {e}")
            await self.store_experience(f"Failed cycle due to error: {e}", type="error")
            return f"Cycle Failed: {e}"
