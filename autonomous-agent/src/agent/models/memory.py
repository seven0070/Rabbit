import datetime
import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.agent.models.base import Base


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    identity_id: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String)  # 'episodic', 'semantic', 'procedural'
    content: Mapped[str] = mapped_column(String)
    embedding: Mapped[list[float]] = mapped_column(
        Vector(1536), nullable=True
    )  # OpenAI ada-002 dimension size as default
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
