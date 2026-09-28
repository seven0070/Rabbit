# Autonomous Agent

A persistent, autonomous executive system with cognition, memory, agency, verification, controlled evolution, and a separate empirical research layer for consciousness-related properties.

## Architecture

- **Executive Core**: Drives the reasoning, planning, and execution loop.
- **Model Gateway**: A provider-agnostic interface (OpenAI, Anthropic, Ollama).
- **Persistence**: PostgreSQL + pgvector as the source of truth.
- **Subjectivity Research**: Separate telemetry and metrics to track continuity and internal state.
- **Self-Modification**: Strictly gated (Branch -> Build -> Test -> Security -> Benchmark -> Verify -> Approve -> Deploy).

## Setup

1. Copy `.env.example` to `.env` and fill in API keys.
2. Start the database: `docker-compose up -d db`
3. Install dependencies: `pip install -e .[dev]`
4. Run migrations: `alembic upgrade head`
