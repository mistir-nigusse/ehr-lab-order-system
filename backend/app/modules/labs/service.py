"""Labs service layer (placeholders)."""
from .models import LabResult
from .repo import LabResultRepository


class LabsService:
    def __init__(self, repo: LabResultRepository):
        self.repo = repo

    def accept_results(self, order_id: int, results: list[LabResult]) -> None:
        # Idempotency would be handled in repository/DB layer
        self.repo.append_results(order_id, results)

