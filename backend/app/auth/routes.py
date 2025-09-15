import os
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

from ..core.auth import Role
from . import bp


def _load_allowed_users():
    """Load allowed users from AUTH_USERS env. this is configured on backend env t=as rightnow my system doesn;t support registration
    """
    cfg = (os.getenv("AUTH_USERS") or "").strip()
    users: dict[str, dict] = {}
    if not cfg:
        return users
    for entry in cfg.split(","):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split(":")
        if len(parts) not in (3, 4):
            continue
        u, p, role = parts[0], parts[1], parts[2]
        # accept case-insensitive and a few synonyms
        role_key = (role or "").strip().lower()
        role_map = {
            "physician": Role.PHYSICIAN,
            "doctor": Role.PHYSICIAN,
            "md": Role.PHYSICIAN,
            "nurse": Role.NURSE,
            "labtech": Role.LAB_TECH,
            "lab": Role.LAB_TECH,
            "lab_tech": Role.LAB_TECH,
        }
        role_obj = role_map.get(role_key)
        if not role_obj:
            try:
                role_obj = Role(role)
            except Exception:
                continue
        role_value = role_obj.value
        entry = {"password": p, "roles": [role_value]}
        if role_value == Role.LAB_TECH.value:
            # optional 4th part is lab code; else default to env
            lab_code = parts[3] if len(parts) == 4 else os.getenv("DEFAULT_LAB_CODE", "LAB")
            if lab_code:
                entry["lab"] = lab_code
        users[u] = entry
    return users


ALLOWED_USERS = _load_allowed_users()


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    requested_role = (data.get("role") or "").strip()

    if not username or not password:
        return jsonify(error="username and password required"), 400
    if len(password) < 6:
        return jsonify(error="password must be at least 6 characters"), 400

    # If AUTH_USERS configured, enforce whitelist credentials
    if ALLOWED_USERS:
        user = ALLOWED_USERS.get(username)
        if not user or user.get("password") != password:
            return jsonify(error="invalid credentials"), 401
        roles = user.get("roles", [])
        # If client supplied a role, it must match the stored role
        if requested_role and requested_role not in roles:
            return jsonify(error="role not permitted for this user", allowed=roles), 403
        # Include lab code for LabTech
        lab = user.get("lab")
    else:
        # No configured users → deny login (secure default)
        return jsonify(error="authentication not configured", hint="set AUTH_USERS env"), 503

    claims = {"roles": roles}
    if 'LabTech' in roles and lab:
        claims['lab'] = lab
    token = create_access_token(identity=username, additional_claims=claims)
    return jsonify(access_token=token, roles=roles, username=username)


@bp.get("/me")
@jwt_required()
def me():
    identity = get_jwt_identity()
    claims = get_jwt()
    return jsonify(username=identity, roles=claims.get("roles", []))
