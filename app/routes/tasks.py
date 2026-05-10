from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, Response
from flask_login import login_required, current_user
from app import db, socketio
from app.models.task import Task
import csv
import io
from datetime import date

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
    return render_template("dashboard.html", tasks=tasks)


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
        due_date_str = request.form.get("due_date", "").strip()

        error = validate_task_input(title, priority, status)
        if error:
            flash(error, "danger")
            return redirect(url_for("tasks.add_task"))

        # Parse due date if provided
        due_date = None
        if due_date_str:
            try:
                due_date = date.fromisoformat(due_date_str)
            except ValueError:
                flash("Invalid due date format.", "danger")
                return redirect(url_for("tasks.add_task"))

        task = Task(
            user_id=current_user.id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date,
        )
        db.session.add(task)
        db.session.commit()

        # Notify all connected clients about the new task
        socketio.emit("task_event", {"type": "created", "message": f'Task "{title}" created successfully.'})

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
        title        = request.form.get("title", "").strip()
        description  = request.form.get("description", "").strip()
        priority     = request.form.get("priority", task.priority)
        status       = request.form.get("status", task.status)
        due_date_str = request.form.get("due_date", "").strip()

        error = validate_task_input(title, priority, status)
        if error:
            flash(error, "danger")
            return redirect(url_for("tasks.edit_task", task_id=task_id))

        due_date = task.due_date
        if due_date_str:
            try:
                due_date = date.fromisoformat(due_date_str)
            except ValueError:
                flash("Invalid due date format.", "danger")
                return redirect(url_for("tasks.edit_task", task_id=task_id))
        elif due_date_str == "":
            due_date = None

        task.title       = title
        task.description = description
        task.priority    = priority
        task.status      = status
        task.due_date    = due_date
        db.session.commit()

        # Notify all connected clients about the update
        socketio.emit("task_event", {"type": "updated", "message": f'Task "{task.title}" updated.'})

        flash("Task updated successfully!", "success")
        return redirect(url_for("tasks.dashboard"))

    return render_template("tasks/edit_task.html", task=task,
                           priorities=VALID_PRIORITIES,
                           statuses=VALID_STATUSES)


# ─────────────────────────────────────────────
#  TOGGLE COMPLETE
# ─────────────────────────────────────────────

@tasks_bp.route("/tasks/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You don't have permission to update that task.", "danger")
        return redirect(url_for("tasks.dashboard"))

    # Flip between Completed and In Progress
    if task.status == "Completed":
        task.status = "In Progress"
        msg = f'Task "{task.title}" marked as In Progress.'
    else:
        task.status = "Completed"
        msg = f'Task "{task.title}" marked as completed.'

    db.session.commit()
    socketio.emit("task_event", {"type": "updated", "message": msg})
    return redirect(url_for("tasks.dashboard"))


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

    title = task.title
    db.session.delete(task)
    db.session.commit()

    # Notify all connected clients about the deletion
    socketio.emit("task_event", {"type": "deleted", "message": f'Task "{title}" deleted.'})

    flash("Task deleted.", "info")
    return redirect(url_for("tasks.dashboard"))


# ─────────────────────────────────────────────
#  CSV EXPORT
# ─────────────────────────────────────────────

@tasks_bp.route("/tasks/export")
@login_required
def export_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Title", "Description", "Priority", "Status", "Due Date", "Created Date"])
    for t in tasks:
        writer.writerow([
            t.title,
            t.description or "",
            t.priority,
            t.status,
            t.due_date.strftime("%Y-%m-%d") if t.due_date else "",
            t.created_date.strftime("%Y-%m-%d %H:%M"),
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=taskorbit_tasks.csv"}
    )


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
