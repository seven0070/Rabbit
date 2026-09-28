import json
import os
import time
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.agent.core.config import settings
from src.agent.models.subjectivity import SubjectiveState


class SubjectivityObserver:
    """
    Separate experimental subsystem that observes internal state
    and logs measurable experimental data and hypotheses.
    """

    def __init__(self, db_session: AsyncSession, identity_id: str):
        self.db = db_session
        self.identity_id = identity_id

        # Telemetry directory for append-only raw JSONL
        self.telemetry_dir = settings.TELEMETRY_DIR
        os.makedirs(self.telemetry_dir, exist_ok=True)
        self.telemetry_file = os.path.join(
            self.telemetry_dir, f"subjectivity_{self.identity_id}.jsonl"
        )

        # Continuity counter
        self.continuity_index = 0

    async def log_telemetry(self, event_type: str, data: Dict[str, Any]):
        """Raw append-only JSONL event telemetry for experimental traces."""
        payload = {"timestamp": time.time(), "event_type": event_type, "data": data}
        with open(self.telemetry_file, "a") as f:
            f.write(json.dumps(payload) + "\n")

    async def record_state(
        self,
        confidence: float,
        uncertainty: float,
        summary: str,
        attention: str,
        measurements: Dict[str, Any],
        experiment_id: Optional[str] = None,
    ):
        """
        Record structured experimental state to dedicated PostgreSQL tables.
        This represents the objective measurement of 'internal state' variables.
        """
        self.continuity_index += 1

        state_record = SubjectiveState(
            identity_id=self.identity_id,
            confidence_score=confidence,
            uncertainty_level=uncertainty,
            internal_state_summary=summary,
            attention_focus=attention,
            continuity_index=self.continuity_index,
            experiment_id=experiment_id,
            measurements=measurements,
        )

        self.db.add(state_record)
        await self.db.commit()

        # Also log to raw telemetry
        await self.log_telemetry(
            "state_recorded",
            {
                "confidence": confidence,
                "uncertainty": uncertainty,
                "summary": summary,
                "continuity_index": self.continuity_index,
            },
        )

        return state_record.id
