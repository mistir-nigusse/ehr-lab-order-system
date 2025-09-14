from datetime import datetime
from flask import Blueprint, jsonify, request
from . import db
from .models import Patient

api_bp = Blueprint("api", __name__)


@api_bp.get("/ping")
def ping():
    return jsonify(message="pong"), 200


@api_bp.post("/patients")
def create_patient():
    data = request.get_json(force=True)
    mrn = data.get("mrn")
    name = data.get("name")
    dob = data.get("dob")
    gender = data.get("gender")
    if not mrn or not name:
        return jsonify(error="mrn and name are required"), 400
    if Patient.query.filter_by(mrn=mrn).first():
        return jsonify(error="mrn already exists"), 409
    try:
        dob_parsed = datetime.fromisoformat(dob).date() if dob else None
    except ValueError:
        return jsonify(error="invalid dob format"), 400
    patient = Patient(mrn=mrn, name=name, dob=dob_parsed, gender=gender)
    db.session.add(patient)
    db.session.commit()
    return jsonify(patientId=patient.id), 201


@api_bp.get("/patients/search")
def search_patients():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    # exact by id
    if q.isdigit():
        p = Patient.query.get(int(q))
        if p:
            return jsonify([p.to_dict()])
    # fuzzy by name or mrn contains
    results = Patient.query.filter(
        db.or_(Patient.name.ilike(f"%{q}%"), Patient.mrn.ilike(f"%{q}%"))
    ).limit(20)
    return jsonify([p.to_dict() for p in results])

