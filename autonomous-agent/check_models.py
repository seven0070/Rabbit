from src.agent.models.base import Base
from src.agent.models.identity import Identity
from src.agent.models.memory import Memory
from src.agent.models.subjectivity import SubjectiveState

print("Models loaded successfully")
print(f"Tables: {Base.metadata.tables.keys()}")
