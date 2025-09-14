from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from . import db
from .modules.patient.orm import PatientORM
from .modules.ehr.orm import EncounterORM, NoteORM
from flask_jwt_extended import jwt_required, get_jwt_identity
from .core.auth import require_roles, Role

api_bp = Blueprint("api", __name__)


@api_bp.get("/ping")
def ping():
    return jsonify(message="pong"), 200



@api_bp.post("/patients")
def create_patient():
    data = request.get_json(force=True) or {}
    mrn = (data.get("mrn") or "").strip()
    name = (data.get("name") or "").strip()
    dob = (data.get("dob") or "").strip() or None
    gender = (data.get("gender") or "").strip() or None

    if not mrn or not name:
        return jsonify(error="mrn and name are required"), 400

    if db.session.query(PatientORM).filter(PatientORM.mrn == mrn).first():
        return jsonify(error="mrn already exists"), 409

    dob_parsed = None
    if dob:
        try:
            dob_parsed = datetime.fromisoformat(dob).date()
        except ValueError:
            return jsonify(error="invalid dob format"), 400

    p = PatientORM(mrn=mrn, name=name, dob=dob_parsed, gender=gender)
    db.session.add(p)
    db.session.commit()
    return jsonify(patientId=p.id), 201


@api_bp.get("/patients/<int:patient_id>/summary")
def patient_summary(patient_id: int):
    return jsonify(error="Not Implemented", hint="FR-2 patient summary", patientId=patient_id), 501


@api_bp.post("/encounters")
@jwt_required()
def create_encounter():
    require_roles(Role.PHYSICIAN, Role.NURSE)
    data = request.get_json(force=True) or {}
    patient_id = data.get("patientId")
    enc_type = (data.get("type") or "").strip().upper()
    started_at = data.get("started_at")

    if not isinstance(patient_id, int):
        return jsonify(error="patientId required"), 400
    if enc_type not in {"OUT", "ER", "IN"}:
        return jsonify(error="type must be one of OUT|ER|IN"), 400

    # Validate patient exists
    if not db.session.get(PatientORM, patient_id):
        return jsonify(error="patient not found"), 404

    started = None
    if started_at:
        try:
            started = datetime.fromisoformat(started_at)
        except ValueError:
            return jsonify(error="invalid started_at"), 400

    enc = EncounterORM(patient_id=patient_id, type=enc_type, started_at=started or datetime.utcnow())
    db.session.add(enc)
    db.session.commit()
    return jsonify(encounterId=enc.id), 201


@api_bp.post("/ehr/notes")
@jwt_required()
def append_note():
    require_roles(Role.PHYSICIAN, Role.NURSE)
    data = request.get_json(force=True) or {}
    patient_id = data.get("patientId")
    encounter_id = data.get("encounterId")
    text = (data.get("text") or "").strip()
    author = (data.get("authorId") or get_jwt_identity() or "").strip()

    if not isinstance(patient_id, int) or not isinstance(encounter_id, int):
        return jsonify(error="patientId and encounterId required"), 400
    if not text:
        return jsonify(error="text required"), 400
    if not author:
        return jsonify(error="author required"), 400

    # Validate patient and encounter exist and match
    p = db.session.get(PatientORM, patient_id)
    if not p:
        return jsonify(error="patient not found"), 404
    enc = db.session.get(EncounterORM, encounter_id)
    if not enc or enc.patient_id != patient_id:
        return jsonify(error="encounter not found or mismatched patient"), 404

    note = NoteORM(patient_id=patient_id, encounter_id=encounter_id, author=author, text=text)
    db.session.add(note)
    db.session.commit()
    return jsonify(noteId=note.id), 201


@api_bp.get("/patients/search")
def search_patients():
    q = (request.args.get("q", "") or "").strip()
    if not q:
        return jsonify([])
    # exact by id
    if q.isdigit():
        p = db.session.get(PatientORM, int(q))
        if p:
            return jsonify([p.to_dict()])
        return jsonify([])
    # fuzzy by name or mrn contains
    results = (
        db.session.query(PatientORM)
        .filter(or_(PatientORM.name.ilike(f"%{q}%"), PatientORM.mrn.ilike(f"%{q}%")))
        .limit(20)
        .all()
    )
    return jsonify([p.to_dict() for p in results])


# Orders & Labs
@api_bp.post("/orders/lab")
def place_lab_order():
    _ = request.get_json(silent=True)
    return jsonify(error="Not Implemented", hint="FR-5 place lab order"), 501


@api_bp.patch("/orders/lab/<int:order_id>/status")
def update_order_status(order_id: int):
    _ = request.get_json(silent=True)
    return jsonify(error="Not Implemented", hint="FR-6 update status", orderId=order_id), 501


@api_bp.get("/orders/lab/<int:order_id>")
def get_lab_order(order_id: int):
    return jsonify(error="Not Implemented", hint="FR-6/FR-7 get order", orderId=order_id), 501


@api_bp.post("/labs/results")
def accept_lab_results():
    _ = request.get_json(silent=True)
    return jsonify(error="Not Implemented", hint="FR-7 accept results"), 501
