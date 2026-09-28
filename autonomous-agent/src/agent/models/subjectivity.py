import datetime
import uuid

from sqlalchemy import JSON, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.agent.models.base import Base


class SubjectiveState(Base):
    """
    Dedicated table for the Subjectivity Research Layer.
    Stores measurable experiments and hypotheses about internal state.
    """

    __tablename__ = "subjective_states"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    identity_id: Mapped[str] = mapped_column(String, index=True)

    # Metacognition metrics
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    uncertainty_level: Mapped[float] = mapped_column(Float, nullable=True)

    # State tracking
    internal_state_summary: Mapped[str] = mapped_column(String, nullable=True)
    attention_focus: Mapped[str] = mapped_column(String, nullable=True)

    # Experiential / Continuity markers
    continuity_index: Mapped[int] = mapped_column(Integer, default=0)
    experiment_id: Mapped[str] = mapped_column(String, nullable=True, index=True)

    measurements: Mapped[dict] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
