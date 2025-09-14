"""Labs repositories (placeholders)."""
from typing import Protocol, Iterable
from .models import LabResult


class LabResultRepository(Protocol):
    def append_results(self, order_id: int, results: list[LabResult]) -> None: ...
    def list_by_order(self, order_id: int) -> Iterable[LabResult]: ...

