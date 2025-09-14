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


class ProblemORM(db.Model):
    __tablename__ = "problems"
    __table_args__ = {"schema": "ehr"}

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient.patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    code = db.Column(db.String(64), nullable=True)
    text = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    onset_date = db.Column(db.Date, nullable=True)
    author = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class AllergyORM(db.Model):
    __tablename__ = "allergies"
    __table_args__ = {"schema": "ehr"}

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient.patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    substance_code = db.Column(db.String(64), nullable=True)
    severity = db.Column(db.String(32), nullable=True)
    reaction = db.Column(db.String(128), nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    author = db.Column(db.String(128), nullable=True)


class MedicationORM(db.Model):
    __tablename__ = "medications"
    __table_args__ = {"schema": "ehr"}

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patient.patients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rx_code = db.Column(db.String(64), nullable=True)
    dose = db.Column(db.String(64), nullable=True)
    route = db.Column(db.String(64), nullable=True)
    start = db.Column(db.Date, nullable=True)
    end = db.Column(db.Date, nullable=True)
    author = db.Column(db.String(128), nullable=True)
