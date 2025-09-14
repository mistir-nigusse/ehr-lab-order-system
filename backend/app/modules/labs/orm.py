from datetime import datetime
from app import db  # type: ignore


class LabResultORM(db.Model):
    __tablename__ = "results"
    __table_args__ = {"schema": "labs"}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    test_code = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(255), nullable=True)
    units = db.Column(db.String(64), nullable=True)
    ref_range = db.Column(db.String(128), nullable=True)
    status = db.Column(db.String(32), nullable=True)
    resulted_at = db.Column(db.DateTime, nullable=True)
    received_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    digest = db.Column(db.String(64), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "test_code": self.test_code,
            "value": self.value,
            "units": self.units,
            "ref_range": self.ref_range,
            "status": self.status,
            "resulted_at": self.resulted_at.isoformat() if self.resulted_at else None,
            "received_at": self.received_at.isoformat() if self.received_at else None,
        }

