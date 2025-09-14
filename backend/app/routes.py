from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from . import db
from .modules.patient.orm import PatientORM

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
def create_encounter():
    _ = request.get_json(silent=True)
    return jsonify(error="Not Implemented", hint="FR-3 create encounter"), 501


@api_bp.post("/ehr/notes")
def append_note():
    _ = request.get_json(silent=True)
    return jsonify(error="Not Implemented", hint="FR-3 append-only notes"), 501


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
