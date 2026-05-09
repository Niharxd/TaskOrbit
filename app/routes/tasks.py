from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__)

VALID_PRIORITIES = ["Low", "Medium", "High"]
VALID_STATUSES   = ["Pending", "In Progress", "Completed"]


# ─────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────

def validate_task_input(title, priority, status):
    """Returns an error string or None if everything is fine."""
    if not title or not title.strip():
        return "Task title is required."
    if priority not in VALID_PRIORITIES:
        return "Invalid priority value."
    if status not in VALID_STATUSES:
        return "Invalid status value."
    return None


# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────

@tasks_bp.route("/dashboard")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()

    # Simple stats for the summary cards
    stats = {
        "total":       len(tasks),
        "pending":     sum(1 for t in tasks if t.status == "Pending"),
        "in_progress": sum(1 for t in tasks if t.status == "In Progress"),
        "completed":   sum(1 for t in tasks if t.status == "Completed"),
    }

    return render_template("dashboard.html", tasks=tasks, stats=stats)


# ─────────────────────────────────────────────
#  ADD TASK
# ─────────────────────────────────────────────

@tasks_bp.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority    = request.form.get("priority", "Medium")
        status      = request.form.get("status", "Pending")

        error = validate_task_input(title, priority, status)
        if error:
            flash(error, "danger")
            return redirect(url_for("tasks.add_task"))

        task = Task(
            user_id=current_user.id,
            title=title,
            description=description,
            priority=priority,
            status=status,
        )
        db.session.add(task)
        db.session.commit()

        flash("Task added successfully!", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("tasks/add_task.html",
                           priorities=VALID_PRIORITIES,
                           statuses=VALID_STATUSES)


# ─────────────────────────────────────────────
#  EDIT TASK
# ─────────────────────────────────────────────

@tasks_bp.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    # 404 if task doesn't exist; 403 if it belongs to someone else
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You don't have permission to edit that task.", "danger")
        return redirect(url_for("tasks.dashboard"))

    if request.method == "POST":
        title       = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority    = request.form.get("priority", task.priority)
        status      = request.form.get("status", task.status)

        error = validate_task_input(title, priority, status)
        if error:
            flash(error, "danger")
            return redirect(url_for("tasks.edit_task", task_id=task_id))

        task.title       = title
        task.description = description
        task.priority    = priority
        task.status      = status
        db.session.commit()

        flash("Task updated successfully!", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("tasks/edit_task.html", task=task,
                           priorities=VALID_PRIORITIES,
                           statuses=VALID_STATUSES)


# ─────────────────────────────────────────────
#  DELETE TASK
# ─────────────────────────────────────────────

@tasks_bp.route("/tasks/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You don't have permission to delete that task.", "danger")
        return redirect(url_for("tasks.dashboard"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "info")
    return redirect(url_for("tasks.dashboard"))


# ─────────────────────────────────────────────
#  REST API
# ─────────────────────────────────────────────

@tasks_bp.route("/api/tasks", methods=["GET"])
@login_required
def api_get_tasks():
    """GET /api/tasks — return all tasks for the logged-in user."""
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route("/api/tasks", methods=["POST"])
@login_required
def api_create_task():
    """POST /api/tasks — create a new task from JSON body."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    title       = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    priority    = data.get("priority", "Medium")
    status      = data.get("status", "Pending")

    error = validate_task_input(title, priority, status)
    if error:
        return jsonify({"error": error}), 422

    task = Task(user_id=current_user.id, title=title,
                description=description, priority=priority, status=status)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
@login_required
def api_update_task(task_id):
    """PUT /api/tasks/<id> — update an existing task."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Forbidden."}), 403

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    title       = (data.get("title") or task.title).strip()
    description = (data.get("description") or task.description or "").strip()
    priority    = data.get("priority", task.priority)
    status      = data.get("status", task.status)

    error = validate_task_input(title, priority, status)
    if error:
        return jsonify({"error": error}), 422

    task.title       = title
    task.description = description
    task.priority    = priority
    task.status      = status
    db.session.commit()
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def api_delete_task(task_id):
    """DELETE /api/tasks/<id> — delete a task."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Forbidden."}), 403

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted."}), 200
