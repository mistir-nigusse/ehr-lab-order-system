from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Encounter:
    id: Optional[int]
    patient_id: int
    type: str
    started_at: Optional[datetime] = None
    status: Optional[str] = None


@dataclass
class Problem:
    id: Optional[int]
    patient_id: int
    code: Optional[str]
    text: Optional[str]
    active: bool = True
    onset_date: Optional[date] = None
    author: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class Allergy:
    id: Optional[int]
    patient_id: int
    substance_code: Optional[str]
    severity: Optional[str]
    reaction: Optional[str]
    recorded_at: Optional[datetime] = None
    author: Optional[str] = None


@dataclass
class Medication:
    id: Optional[int]
    patient_id: int
    rx_code: Optional[str]
    dose: Optional[str]
    route: Optional[str]
    start: Optional[date] = None
    end: Optional[date] = None
    author: Optional[str] = None

