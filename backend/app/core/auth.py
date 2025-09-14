from enum import Enum
from flask import abort
from flask_jwt_extended import get_jwt


class Role(str, Enum):
    PHYSICIAN = "Physician"
    NURSE = "Nurse"
    LAB_TECH = "LabTech"


class AuthContext:
    """Placeholder for authenticated user context.

    In real implementation, integrate with Flask-JWT-Extended to populate
    identity and roles for RBAC checks.
    """

    def __init__(self, user_id: str | None = None, roles: list[Role] | None = None):
        self.user_id = user_id
        self.roles = roles or []

    def has_role(self, role: Role) -> bool:
        return role in self.roles


def require_roles(*allowed: Role):
    """
    for inline checks inside route handlers.
    """
    claims = get_jwt()
    token_roles = set(claims.get("roles", []))
    if not token_roles.intersection({r.value for r in allowed}):
        abort(403, description="insufficient role")
