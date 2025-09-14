from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from . import db
from .modules.patient.orm import PatientORM
from .modules.ehr.orm import EncounterORM, NoteORM
from flask_jwt_extended import jwt_required, get_jwt_identity
from .core.auth import require_roles, Role
from .modules.orders.orm import OrderORM
from .modules.labs.orm import LabResultORM
from sqlalchemy.dialects.postgresql import insert as pg_insert
import hashlib, json

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
@jwt_required()
def place_lab_order():
    require_roles(Role.PHYSICIAN, Role.NURSE)
    data = request.get_json(force=True) or {}
    encounter_id = data.get("encounterId")
    tests = data.get("tests")

    if not isinstance(encounter_id, int):
        return jsonify(error="encounterId required"), 400
    if not isinstance(tests, list) or not all(isinstance(t, str) and t.strip() for t in tests):
        return jsonify(error="tests must be a non-empty array of strings"), 400

    enc = db.session.get(EncounterORM, encounter_id)
    if not enc:
        return jsonify(error="encounter not found"), 404

    ordered_by = get_jwt_identity() or None
    order = OrderORM(encounter_id=encounter_id, tests=[t.strip() for t in tests], ordered_by=ordered_by)
    db.session.add(order)
    db.session.commit()
    return jsonify(orderId=order.id), 201


@api_bp.patch("/orders/lab/<int:order_id>/status")
@jwt_required()
def update_order_status(order_id: int):
    require_roles(Role.PHYSICIAN, Role.NURSE, Role.LAB_TECH)
    data = request.get_json(force=True) or {}
    status = (data.get("status") or "").strip().lower()
    allowed = {"ordered", "collected", "in_progress", "resulted", "corrected"}
    if status not in allowed:
        return jsonify(error=f"status must be one of {sorted(allowed)}"), 400

    order = db.session.get(OrderORM, order_id)
    if not order:
        return jsonify(error="order not found"), 404
    order.status = status
    db.session.commit()
    return jsonify(ok=True)


@api_bp.get("/orders/lab/<int:order_id>")
def get_lab_order(order_id: int):
    order = db.session.get(OrderORM, order_id)
    if not order:
        return jsonify(error="order not found"), 404
    results = (
        db.session.query(LabResultORM)
        .filter(LabResultORM.order_id == order_id)
        .order_by(LabResultORM.resulted_at.is_(None), LabResultORM.resulted_at.desc().nullslast())
        .all()
    )
    return jsonify(order=order.to_dict(), results=[r.to_dict() for r in results])


@api_bp.post("/labs/results")
def accept_lab_results():
    data = request.get_json(force=True) or {}
    order_id = data.get("orderId")
    results = data.get("results")

    if not isinstance(order_id, int):
        return jsonify(error="orderId required"), 400
    if not isinstance(results, list) or not results:
        return jsonify(error="results must be a non-empty array"), 400

    order = db.session.get(OrderORM, order_id)
    if not order:
        return jsonify(error="order not found"), 404

    # Prepare rows with digest for idempotency
    inserted = 0
    for item in results:
        if not isinstance(item, dict):
            continue
        test_code = (item.get("test_code") or "").strip()
        value = (item.get("value") or None)
        units = (item.get("units") or None)
        ref_range = (item.get("ref_range") or None)
        status = (item.get("status") or None)
        resulted_at = item.get("resulted_at") or None
        if not test_code:
            continue
        # Canonicalize the payload relevant fields for digest
        digest_input = json.dumps(
            {
                "test_code": test_code,
                "value": value,
                "units": units,
                "ref_range": ref_range,
                "status": status,
                "resulted_at": resulted_at,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        digest = hashlib.sha256(digest_input.encode("utf-8")).hexdigest()

        # Parse resulted_at if provided
        ra = None
        if resulted_at:
            try:
                ra = datetime.fromisoformat(resulted_at)
            except ValueError:
                ra = None

        stmt = pg_insert(LabResultORM.__table__).values(
            order_id=order_id,
            test_code=test_code,
            value=value,
            units=units,
            ref_range=ref_range,
            status=status,
            resulted_at=ra,
            digest=digest,
        ).on_conflict_do_nothing(constraint='uq_results_order_digest')
        db.session.execute(stmt)
    db.session.commit()
    return jsonify(ok=True), 200
