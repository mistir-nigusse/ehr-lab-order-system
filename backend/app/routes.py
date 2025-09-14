from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__)


@api_bp.get("/ping")
def ping():
    return jsonify(message="pong"), 200



@api_bp.post("/patients")
def create_patient():
    _ = request.get_json(silent=True)
    return jsonify(error="Not Implemented", hint="FR-1 create patient"), 501


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
    _ = request.args.get("q", "")
    return jsonify(error="Not Implemented", hint="FR-4 search"), 501


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
