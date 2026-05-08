from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Registration page.
    GET  — show the form
    POST — process the form data
    """
    # If user is already logged in, send them to home
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # --- Basic validation ---
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect(url_for("auth.register"))

        # --- Check for duplicates ---
        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("That username is already taken.", "danger")
            return redirect(url_for("auth.register"))

        # --- Create and save the new user ---
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Login page.
    GET  — show the form
    POST — validate credentials and log the user in
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=email).first()

        # Check user exists and password is correct
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")

            # Redirect to the page they were trying to visit, or home
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.home"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Log the user out and redirect to home."""
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("main.home"))
