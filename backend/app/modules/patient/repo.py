"""Repository abstraction for patient persistence (placeholder)."""
from typing import Protocol, Iterable, Optional
from .models import Patient


class PatientRepository(Protocol):
    def get(self, patient_id: int) -> Optional[Patient]:
        ...

    def find_by_mrn(self, mrn: str) -> Optional[Patient]:
        ...

    def search(self, q: str, limit: int = 20) -> Iterable[Patient]:
        ...

    def create(self, patient: Patient) -> int:
        ...


class SqlAlchemyPatientRepository:
    """Placeholder implementation to be wired to SQLAlchemy models later."""

    def __init__(self):
        pass

    def get(self, patient_id: int) -> Optional[Patient]:
        return None

    def find_by_mrn(self, mrn: str) -> Optional[Patient]:
        return None

    def search(self, q: str, limit: int = 20) -> Iterable[Patient]:
        return []

    def create(self, patient: Patient) -> int:
        return 0

