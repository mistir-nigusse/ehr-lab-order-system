from flask import Blueprint

bp = Blueprint("auth", __name__)

# Ensure routes register with the blueprint on import
from . import routes  # noqa: E402,F401
