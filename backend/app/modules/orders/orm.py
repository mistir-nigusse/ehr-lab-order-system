from datetime import datetime
from app import db  # type: ignore
from sqlalchemy.dialects.postgresql import JSONB


class OrderORM(db.Model):
    __tablename__ = "orders"
    __table_args__ = {"schema": "orders"}

    id = db.Column(db.Integer, primary_key=True)
    encounter_id = db.Column(
        db.Integer,
        db.ForeignKey("ehr.encounters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tests = db.Column(JSONB, nullable=False)
    status = db.Column(db.String(16), nullable=False, default="ordered")
    ordered_by = db.Column(db.String(128), nullable=True)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "encounter_id": self.encounter_id,
            "tests": self.tests,
            "status": self.status,
            "ordered_by": self.ordered_by,
            "placed_at": self.placed_at.isoformat() if self.placed_at else None,
        }

