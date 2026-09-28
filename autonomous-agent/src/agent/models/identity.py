import uuid

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from src.agent.models.base import Base


class Identity(Base):
    __tablename__ = "identities"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    purpose: Mapped[str] = mapped_column(String)
    core_directives: Mapped[list[str]] = mapped_column(JSON, default=list)
    state: Mapped[dict] = mapped_column(
        JSON, default=dict
    )  # E.g., status, current goal ID
