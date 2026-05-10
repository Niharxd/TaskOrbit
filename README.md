# TaskOrbit

> Stay in orbit, stay productive.

TaskOrbit is a full-stack task management web application built with Flask and PostgreSQL. It provides a secure, user-specific dashboard for creating and tracking tasks, a real-time notification system using WebSockets, and an analytics module powered by Pandas and NumPy.

---

## Screenshots

| Home | Dashboard |
|------|----------|
| ![Home](app/static/images/home.png) | ![Dashboard](app/static/images/dashboard.png) |

| Analytics | Profile |
|-----------|--------|
| ![Analytics](app/static/images/analytics.png) | ![Profile](app/static/images/profile.png) |

| Login | Register |
|-------|----------|
| ![Login](app/static/images/login.png) | ![Register](app/static/images/register.png) |

| Add Task |
|----------|
| ![Add Task](app/static/images/addtask.png) |

---

## Features

- User registration and login with input validation
- Secure password hashing using Werkzeug
- Session-based authentication with Flask-Login
- Protected routes - unauthenticated users are redirected to login
- Flash messages for all user-facing actions
- Task dashboard with summary statistics and progress tracking
- Full task CRUD - create, read, update, delete
- Priority levels - Low, Medium, High
- Status tracking - Pending, In Progress, Completed
- Due dates with overdue detection and highlighting
- One-click task completion toggle
- CSV export for all tasks
- REST API for all task operations (JSON responses)
- Analytics dashboard with Pandas and NumPy processing
- Pie and bar charts using Chart.js
- Real-time WebSocket notifications using Flask-SocketIO
- Profile page with account details and task summary
- Responsive dark-space UI built with Bootstrap 5

---

## Tech Stack

| Technology       | Purpose                              |
|------------------|--------------------------------------|
| Python 3.10+     | Backend language                     |
| Flask            | Web framework                        |
| PostgreSQL       | Relational database                  |
| Flask-SQLAlchemy | ORM for database interaction         |
| Flask-Login      | User session management              |
| Flask-SocketIO   | WebSocket support                    |
| Werkzeug         | Password hashing                     |
| Pandas           | Task data processing and analysis    |
| NumPy            | Statistical calculations             |
| Bootstrap 5      | Frontend UI framework                |
| Chart.js         | Frontend charts                      |
| python-dotenv    | Environment variable management      |

---

## Project Structure

```
taskorbit/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Home page route
│   │   ├── auth.py          # Login, Register, Logout
│   │   ├── tasks.py         # Task CRUD + REST API + SocketIO events
│   │   ├── analytics.py     # Analytics page route
│   │   └── profile.py       # Profile page route
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── services/
│   │   └── analytics.py     # Pandas + NumPy analytics logic
│   ├── templates/
│   │   ├── base.html        # Base layout (navbar, footer, toast container)
│   │   ├── home.html        # Landing page
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   ├── dashboard.html   # Task dashboard
│   │   ├── analytics.html   # Analytics page with charts
│   │   ├── profile.html     # User profile page
│   │   └── tasks/
│   │       ├── add_task.html
│   │       └── edit_task.html
│   ├── static/
│   │   ├── css/style.css    # Custom dark-space theme
│   │   ├── js/main.js       # UI helpers + SocketIO toast logic
│   │   └── images/          # Screenshots and assets
│   └── __init__.py          # App factory with SocketIO init
│
├── database/
│   └── schema.sql           # PostgreSQL schema (reference)
├── instance/
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Niharxd/TaskOrbit.git
cd TaskOrbit/taskorbit
```

### 2. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

### 1. Create a database

```sql
CREATE DATABASE taskorbit_db;
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskorbit_db
```

> The `.env` file is listed in `.gitignore` and should never be committed to version control.

The `database/schema.sql` file contains the raw SQL schema for reference. Flask-SQLAlchemy creates the tables automatically on first run.

---

## Running the Application

```bash
# Windows
venv\Scripts\activate
python run.py

# macOS / Linux
source venv/bin/activate
python run.py
```

Visit: **http://127.0.0.1:5000**

Database tables are created automatically on first run.

---

## Task Management

After logging in, users land on the dashboard which shows:

- A personalized welcome message with task summary
- Four stat cards - Total, Pending, In Progress, Completed
- An overall completion progress bar
- A full task list with priority, status, and due date badges
- One-click Done / Undo toggle per task
- Edit, Delete, and Export CSV actions
- Overdue tasks highlighted in red
- An empty state prompt when no tasks exist

### Task Fields

| Field        | Type     | Details                             |
|--------------|----------|-------------------------------------|
| Title        | String   | Required, max 200 characters        |
| Description  | Text     | Optional                            |
| Priority     | String   | Low / Medium / High                 |
| Status       | String   | Pending / In Progress / Completed   |
| Due Date     | Date     | Optional, enables overdue detection |
| Created Date | DateTime | Auto-generated on creation          |

---

## REST API

All endpoints require an active login session.

### GET /api/tasks

Returns all tasks for the authenticated user.

**Response 200**
```json
[
  {
    "id": 1,
    "title": "Build the dashboard",
    "description": "Create the main dashboard UI",
    "priority": "High",
    "status": "In Progress",
    "due_date": "2025-02-01",
    "created_date": "2025-01-15 10:30"
  }
]
```

### POST /api/tasks

Creates a new task.

**Request body**
```json
{
  "title": "Write unit tests",
  "description": "Cover all route handlers",
  "priority": "Medium",
  "status": "Pending"
}
```

**Response 201** - Returns the created task object.

### PUT /api/tasks/\<id\>

Updates an existing task. Send only the fields you want to change.

**Response 200** - Returns the updated task object.
**Response 403** - Task belongs to a different user.

### DELETE /api/tasks/\<id\>

Deletes a task permanently.

**Response 200**
```json
{ "message": "Task deleted." }
```

**Response 403** - Task belongs to a different user.

---

## Analytics Module

The analytics page is available at `/analytics` after logging in.

It uses:
- **Pandas** to load task data into a DataFrame and compute value counts
- **NumPy** to calculate the completion percentage
- **Chart.js** to render a doughnut chart (status distribution) and a bar chart (priority distribution)

Metrics displayed:
- Total tasks
- Completed, Pending, In Progress counts
- Completion rate percentage
- Status distribution chart
- Priority distribution chart and breakdown

---

## WebSocket Notifications

TaskOrbit uses Flask-SocketIO to broadcast real-time notifications to all connected clients whenever a task is created, updated, or deleted.

The frontend connects automatically when a user is logged in. Notifications appear as small toast messages in the bottom-right corner without requiring a page refresh.

Events emitted:
- `task_event` with type `created` - when a task is added
- `task_event` with type `updated` - when a task is edited
- `task_event` with type `deleted` - when a task is removed

---

## Future Improvements

- Task filtering and search
- Dark/light mode toggle
- Email notifications
- Deploy to production

---

## Demo

> Add a demo video or live link here once deployed.

---

## Author

**Nihar Ranjan Patra**

- GitHub: [github.com/Niharxd](https://github.com/Niharxd)
- LinkedIn: [linkedin.com/in/nihar-patra-2277np](https://www.linkedin.com/in/nihar-patra-2277np/)
- LeetCode: [leetcode.com/u/Nihar_Patra](https://leetcode.com/u/Nihar_Patra/)
