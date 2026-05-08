from flask import Blueprint, render_template
from flask_login import current_user

# Blueprint groups related routes together
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Landing page — shown to everyone, logged in or not."""
    return render_template("home.html")
