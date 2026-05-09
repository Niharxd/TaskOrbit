from app import db
from datetime import datetime


class Task(db.Model):
    """
    Task model — each task belongs to a specific user.
    Users can only see and manage their own tasks.
    """
    __tablename__ = "tasks"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, nullable=True)
    priority     = db.Column(db.String(20), nullable=False, default="Medium")   # Low / Medium / High
    status       = db.Column(db.String(20), nullable=False, default="Pending")  # Pending / In Progress / Completed
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to the user who owns this task
    user = db.relationship("User", backref=db.backref("tasks", lazy=True))

    def to_dict(self):
        """Return a plain dict — useful for the REST API responses."""
        return {
            "id":           self.id,
            "title":        self.title,
            "description":  self.description or "",
            "priority":     self.priority,
            "status":       self.status,
            "created_date": self.created_date.strftime("%Y-%m-%d %H:%M"),
        }

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"
