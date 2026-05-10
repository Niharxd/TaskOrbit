from app import db
from datetime import datetime, date


class Task(db.Model):
    __tablename__ = "tasks"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text, nullable=True)
    priority     = db.Column(db.String(20), nullable=False, default="Medium")
    status       = db.Column(db.String(20), nullable=False, default="Pending")
    due_date     = db.Column(db.Date, nullable=True)  # optional due date
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("tasks", lazy=True))

    @property
    def is_overdue(self):
        """True if task has a due date, is not completed, and the date has passed."""
        return (
            self.due_date is not None
            and self.status != "Completed"
            and self.due_date < date.today()
        )

    def to_dict(self):
        return {
            "id":           self.id,
            "title":        self.title,
            "description":  self.description or "",
            "priority":     self.priority,
            "status":       self.status,
            "due_date":     self.due_date.strftime("%Y-%m-%d") if self.due_date else None,
            "created_date": self.created_date.strftime("%Y-%m-%d %H:%M"),
        }

    def __repr__(self):
        return f"<Task {self.id}: {self.title}>"
