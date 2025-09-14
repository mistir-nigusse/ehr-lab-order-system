"""EHR service layer (placeholders)."""
from .models import Encounter, Problem, Allergy, Medication
from .repo import (
    EncounterRepository,
    ProblemRepository,
    AllergyRepository,
    MedicationRepository,
)


class EHRService:
    def __init__(
        self,
        encounters: EncounterRepository,
        problems: ProblemRepository,
        allergies: AllergyRepository,
        medications: MedicationRepository,
    ):
        self.encounters = encounters
        self.problems = problems
        self.allergies = allergies
        self.medications = medications

    # Placeholder methods
    def create_encounter(self, encounter: Encounter) -> int:
        return self.encounters.create(encounter)

