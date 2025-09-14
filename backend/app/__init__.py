import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    elif os.getenv("USE_SQLITE") == "1":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ehr_dev.db"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER','ehr')}:{os.getenv('POSTGRES_PASSWORD','ehrpw')}"
            f"@{os.getenv('POSTGRES_HOST','postgres')}:{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('POSTGRES_DB','ehrdb')}"
        )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "dev-insecure-change-me")

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)

    from .models import Patient  # noqa: F401
    from .routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    with app.app_context():
        db.create_all()

    return app
