from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

from ..core.auth import Role
from . import bp


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    role = (data.get("role") or "").strip()

    if not username or not password:
        return jsonify(error="username and password required"), 400

    # DEV-ONLY: accept any credentials; validate role to known set if provided
    roles = []
    if role:
        try:
            roles = [Role(role).value]
        except ValueError:
            return jsonify(error="invalid role", allowed=[r.value for r in Role]), 400

    claims = {"roles": roles}
    token = create_access_token(identity=username, additional_claims=claims)
    return jsonify(access_token=token, roles=roles, username=username)


@bp.get("/me")
@jwt_required()
def me():
    identity = get_jwt_identity()
    claims = get_jwt()
    return jsonify(username=identity, roles=claims.get("roles", []))

