from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class BaseDTO:
    created_at: Optional[datetime] = None


@dataclass
class PatientDTO(BaseDTO):
    id: Optional[int] = None
    mrn: str | None = None
    name: str | None = None
    dob: Optional[date] = None
    gender: Optional[str] = None


@dataclass
class EncounterDTO(BaseDTO):
    id: Optional[int] = None
    patient_id: Optional[int] = None
    type: Optional[str] = None
    started_at: Optional[datetime] = None
    status: Optional[str] = None


@dataclass
class ProblemDTO(BaseDTO):
    id: Optional[int] = None
    patient_id: Optional[int] = None
    code: Optional[str] = None
    text: Optional[str] = None
    active: bool = True
    onset_date: Optional[date] = None
    author: Optional[str] = None


@dataclass
class AllergyDTO(BaseDTO):
    id: Optional[int] = None
    patient_id: Optional[int] = None
    substance_code: Optional[str] = None
    severity: Optional[str] = None
    reaction: Optional[str] = None
    recorded_at: Optional[datetime] = None
    author: Optional[str] = None


@dataclass
class MedicationDTO(BaseDTO):
    id: Optional[int] = None
    patient_id: Optional[int] = None
    rx_code: Optional[str] = None
    dose: Optional[str] = None
    route: Optional[str] = None
    start: Optional[date] = None
    end: Optional[date] = None
    author: Optional[str] = None


@dataclass
class OrderDTO(BaseDTO):
    id: Optional[int] = None
    encounter_id: Optional[int] = None
    tests: list[str] | None = None
    status: Optional[str] = None
    ordered_by: Optional[str] = None
    placed_at: Optional[datetime] = None


@dataclass
class LabResultDTO(BaseDTO):
    id: Optional[int] = None
    order_id: Optional[int] = None
    test_code: Optional[str] = None
    value: Optional[str] = None
    units: Optional[str] = None
    ref_range: Optional[str] = None
    status: Optional[str] = None
    resulted_at: Optional[datetime] = None

