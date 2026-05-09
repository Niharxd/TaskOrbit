from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Landing page — logged-in users get a dashboard link in the hero."""
    return render_template("home.html")
