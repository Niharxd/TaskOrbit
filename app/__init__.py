import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-dev-key-change-this")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    from app.routes.analytics import analytics_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(profile_bp)

    # Inject task stats into every template so the navbar badge always works
    @app.context_processor
    def inject_nav_stats():
        from flask_login import current_user
        if current_user.is_authenticated:
            from app.models.task import Task
            tasks = Task.query.filter_by(user_id=current_user.id).all()
            return {"stats": {
                "total":       len(tasks),
                "completed":   sum(1 for t in tasks if t.status == "Completed"),
                "pending":     sum(1 for t in tasks if t.status == "Pending"),
                "in_progress": sum(1 for t in tasks if t.status == "In Progress"),
            }}
        return {"stats": None}

    with app.app_context():
        from app.models import user, task  # noqa: F401
        db.create_all()

    return app
