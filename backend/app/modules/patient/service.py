"""Patient use-cases/service layer (placeholder)."""
from .models import Patient as PatientDomain
from .repo import PatientRepository


class PatientService:
    def __init__(self, repo: PatientRepository):
        self.repo = repo

    def create_patient(self, mrn: str, name: str) -> int:
        patient = PatientDomain(id=None, mrn=mrn, name=name)
        return self.repo.create(patient)

    def search_patients(self, q: str):
        return list(self.repo.search(q))

