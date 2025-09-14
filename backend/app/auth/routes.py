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
        if len(parts) != 3:
            continue
        u, p, role = parts
        try:
            role_value = Role(role).value
        except Exception:
            # skip invalid role labels
            continue
        users[u] = {"password": p, "roles": [role_value]}
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

    # If AUTH_USERS configured, enforce whitelist credentials
    if ALLOWED_USERS:
        user = ALLOWED_USERS.get(username)
        if not user or user.get("password") != password:
            return jsonify(error="invalid credentials"), 401
        roles = user.get("roles", [])
        # If client supplied a role, it must match the stored role
        if requested_role and requested_role not in roles:
            return jsonify(error="role not permitted for this user", allowed=roles), 403
    else:
        # No configured users → deny login (secure default)
        return jsonify(error="authentication not configured", hint="set AUTH_USERS env"), 503

    claims = {"roles": roles}
    token = create_access_token(identity=username, additional_claims=claims)
    return jsonify(access_token=token, roles=roles, username=username)


@bp.get("/me")
@jwt_required()
def me():
    identity = get_jwt_identity()
    claims = get_jwt()
    return jsonify(username=identity, roles=claims.get("roles", []))
