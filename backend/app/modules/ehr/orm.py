from datetime import datetime
from app import db  # type: ignore


class EncounterORM(db.Model):
    __tablename__ = "encounters"
    __table_args__ = {"schema": "ehr"}

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient.patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = db.Column(db.String(8), nullable=False)  # OUT | ER | IN
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(16), nullable=True)


class NoteORM(db.Model):
    __tablename__ = "notes"
    __table_args__ = {"schema": "ehr"}

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient.patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    encounter_id = db.Column(
        db.Integer,
        db.ForeignKey("ehr.encounters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

