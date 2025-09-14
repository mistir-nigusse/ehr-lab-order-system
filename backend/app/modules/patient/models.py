"""Patient module domain placeholders.

"""
from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Patient:
    id: Optional[int]
    mrn: str
    name: str
    dob: Optional[date] = None
    gender: Optional[str] = None

