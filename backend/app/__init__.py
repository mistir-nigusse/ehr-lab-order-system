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

    from .routes import api_bp
    from .auth import bp as auth_bp

    # Core API
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    try:
        from .modules.patient import bp as patient_bp
        app.register_blueprint(patient_bp, url_prefix="/api/patient")
    except Exception:
        pass
    try:
        from .modules.ehr import bp as ehr_bp
        app.register_blueprint(ehr_bp, url_prefix="/api/ehr")
    except Exception:
        pass
    try:
        from .modules.orders import bp as orders_bp
        app.register_blueprint(orders_bp, url_prefix="/api/orders")
    except Exception:
        pass
    try:
        from .modules.labs import bp as labs_bp
        app.register_blueprint(labs_bp, url_prefix="/api/labs")
    except Exception:
        pass

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200


    return app
