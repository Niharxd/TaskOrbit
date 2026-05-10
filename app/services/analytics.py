import pandas as pd
import numpy as np


def get_analytics(tasks):
    """
    Takes a list of Task objects and returns a dict of analytics.
    Uses Pandas for data processing and NumPy for calculations.
    """
    # If no tasks, return zeroed-out analytics
    if not tasks:
        return {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "in_progress": 0,
            "completion_pct": 0.0,
            "status_distribution": {"Pending": 0, "In Progress": 0, "Completed": 0},
            "priority_distribution": {"Low": 0, "Medium": 0, "High": 0},
        }

    # Build a DataFrame from the task objects
    df = pd.DataFrame([{
        "title":    t.title,
        "status":   t.status,
        "priority": t.priority,
    } for t in tasks])

    total = len(df)

    # Count each status using value_counts
    status_counts = df["status"].value_counts()
    completed   = int(status_counts.get("Completed", 0))
    pending     = int(status_counts.get("Pending", 0))
    in_progress = int(status_counts.get("In Progress", 0))

    # NumPy for the percentage calculation
    completion_pct = float(np.round((completed / total) * 100, 1)) if total > 0 else 0.0

    # Full distribution dicts (always include all keys so charts don't break)
    status_distribution = {
        "Pending":     pending,
        "In Progress": in_progress,
        "Completed":   completed,
    }

    priority_counts = df["priority"].value_counts()
    priority_distribution = {
        "Low":    int(priority_counts.get("Low", 0)),
        "Medium": int(priority_counts.get("Medium", 0)),
        "High":   int(priority_counts.get("High", 0)),
    }

    return {
        "total":                total,
        "completed":            completed,
        "pending":              pending,
        "in_progress":          in_progress,
        "completion_pct":       completion_pct,
        "status_distribution":  status_distribution,
        "priority_distribution": priority_distribution,
    }
