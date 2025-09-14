"""Orders service layer (placeholders)."""
from .models import Order
from .repo import OrderRepository


class OrdersService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def place_lab_order(self, order: Order) -> int:
        return self.repo.create(order)

    def set_status(self, order_id: int, status: str) -> None:
        self.repo.update_status(order_id, status)

