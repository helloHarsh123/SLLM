from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    openai_key: str
    our_key: str
    db_connection_string: Optional[str] = "sqlite:///llm_history.db"