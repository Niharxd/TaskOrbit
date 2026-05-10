from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.task import Task
from app.services.analytics import get_analytics

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def analytics():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    data  = get_analytics(tasks)
    return render_template("analytics.html", data=data)
