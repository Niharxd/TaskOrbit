from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.task import Task

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def profile():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    stats = {
        "total":       len(tasks),
        "completed":   sum(1 for t in tasks if t.status == "Completed"),
        "pending":     sum(1 for t in tasks if t.status == "Pending"),
        "in_progress": sum(1 for t in tasks if t.status == "In Progress"),
        "overdue":     sum(1 for t in tasks if t.is_overdue),
    }
    return render_template("profile.html", stats=stats)
