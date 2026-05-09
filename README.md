# TaskOrbit

> Stay in orbit, stay productive.

TaskOrbit is a task management and productivity tracking web application built with Flask and PostgreSQL. It provides a clean, secure dashboard for creating, organizing, and tracking tasks — with a full REST API and session-based authentication.

---

## Features

- User registration and login with input validation
- Secure password hashing using Werkzeug
- Session-based authentication with Flask-Login
- Protected routes — unauthenticated users are redirected to login
- Flash messages for all user-facing actions
- Task dashboard with summary statistics
- Full task CRUD — create, read, update, delete
- Priority levels — Low, Medium, High
- Status tracking — Pending, In Progress, Completed
- REST API for all task operations
- Responsive dark-space UI built with Bootstrap 5

---

## Tech Stack

| Technology       | Purpose                         |
|------------------|---------------------------------|
| Python 3.10+     | Backend language                |
| Flask            | Web framework                   |
| PostgreSQL       | Relational database             |
| Flask-SQLAlchemy | ORM for database interaction    |
| Flask-Login      | User session management         |
| Werkzeug         | Password hashing                |
| Bootstrap 5      | Frontend UI framework           |
| python-dotenv    | Environment variable management |

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
│   │   └── tasks.py         # Task CRUD + REST API
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── templates/
│   │   ├── base.html        # Base layout (navbar + footer)
│   │   ├── home.html        # Landing page
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   ├── dashboard.html   # User dashboard
│   │   └── tasks/
│   │       ├── add_task.html
│   │       └── edit_task.html
│   ├── static/
│   │   ├── css/style.css    # Custom dark-space theme
│   │   ├── js/main.js       # UI helpers
│   │   └── images/
│   ├── services/            # Business logic (future use)
│   └── __init__.py          # App factory
│
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
git clone https://github.com/Niharxd/taskorbit.git
cd taskorbit
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

## Database Setup

### 1. Create a PostgreSQL database

```sql
CREATE DATABASE taskorbit_db;
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskorbit_db
```

> The `.env` file is listed in `.gitignore` and should never be committed to version control.

---

## Running the Application

```bash
python run.py
```

Visit: **http://127.0.0.1:5000**

Database tables are created automatically on first run.

---

## Task Management

After logging in, users are directed to the dashboard which displays:

- A personalized welcome message with task summary
- Four stat cards — Total, Pending, In Progress, Completed
- An overall completion progress bar
- A full task list with priority and status badges
- Edit and Delete actions per task
- An empty state prompt when no tasks exist

### Task Fields

| Field        | Type     | Details                             |
|--------------|----------|-------------------------------------|
| Title        | String   | Required, max 200 characters        |
| Description  | Text     | Optional                            |
| Priority     | String   | Low / Medium / High                 |
| Status       | String   | Pending / In Progress / Completed   |
| Created Date | DateTime | Auto-generated on creation          |

---

## REST API

All endpoints require an active login session.

### GET /api/tasks

Returns all tasks belonging to the authenticated user.

**Response 200**
```json
[
  {
    "id": 1,
    "title": "Build the dashboard",
    "description": "Create the main dashboard UI",
    "priority": "High",
    "status": "In Progress",
    "created_date": "2025-01-15 10:30"
  }
]
```

---

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

**Response 201** — Returns the created task object.

---

### PUT /api/tasks/\<id\>

Updates an existing task. Send only the fields you want to change.

**Request body**
```json
{
  "status": "Completed"
}
```

**Response 200** — Returns the updated task object.  
**Response 403** — Task belongs to a different user.

---

### DELETE /api/tasks/\<id\>

Deletes a task permanently.

**Response 200**
```json
{ "message": "Task deleted." }
```

**Response 403** — Task belongs to a different user.

---

## Screenshots

| Page      | Preview        |
|-----------|----------------|
| Home      | ![Home](#)     |
| Login     | ![Login](#)    |
| Dashboard | ![Dashboard](#)|
| Add Task  | ![Add Task](#) |

---

## Author

**Nihar Ranjan Patra**

- GitHub: [github.com/Niharxd](https://github.com/Niharxd)
- LinkedIn: [linkedin.com/in/nihar-patra-2277np](https://www.linkedin.com/in/nihar-patra-2277np/)
- LeetCode: [leetcode.com/u/Nihar_Patra](https://leetcode.com/u/Nihar_Patra/)
