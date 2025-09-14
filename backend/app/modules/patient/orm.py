from datetime import datetime, date
from app import db  # type: ignore


class PatientORM(db.Model):
    __tablename__ = "patients"
    __table_args__ = {"schema": "patient"}

    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "mrn": self.mrn,
            "name": self.name,
            "dob": self.dob.isoformat() if isinstance(self.dob, date) else None,
            "gender": self.gender,
        }
