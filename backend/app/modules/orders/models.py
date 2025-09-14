from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    id: Optional[int]
    encounter_id: int
    tests: list[str]
    status: str = "ordered"
    ordered_by: Optional[str] = None
    placed_at: Optional[datetime] = None

