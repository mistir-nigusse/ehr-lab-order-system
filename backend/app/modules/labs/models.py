from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LabResult:
    id: Optional[int]
    order_id: int
    test_code: str
    value: Optional[str] = None
    units: Optional[str] = None
    ref_range: Optional[str] = None
    status: Optional[str] = None
    resulted_at: Optional[datetime] = None

