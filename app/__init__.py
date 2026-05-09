import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions (not tied to any app yet)
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """
    App factory function — creates and configures the Flask app.
    Using a factory makes it easier to test and scale later.
    """
    app = Flask(__name__, instance_relative_config=True)

    # --- App Configuration ---
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-dev-key-change-this")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Suppresses a warning

    # --- Initialize Extensions with App ---
    db.init_app(app)
    login_manager.init_app(app)

    # Where to redirect users who aren't logged in
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # --- Register Blueprints (route groups) ---
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp)

    # --- Create database tables if they don't exist ---
    with app.app_context():
        from app.models import user, task  # noqa: F401 — import needed to register models
        db.create_all()

    return app
