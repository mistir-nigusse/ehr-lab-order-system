from enum import Enum


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

