# 🪐 TaskOrbit

> **Stay in orbit, stay productive.**

TaskOrbit is a task management and productivity tracking web application built with Flask and PostgreSQL. It lets you create, manage, and track your tasks through a clean dashboard — all behind a secure login system.

---

## ✅ Features

- User Registration with validation
- Secure Login / Logout (session-based)
- Password hashing (no plain-text passwords stored)
- Flash messages for all user actions
- Protected routes (login required)
- **Task Dashboard** with summary stats
- **Full Task CRUD** — Add, Edit, Delete, View tasks
- **Priority levels** — Low / Medium / High
- **Status tracking** — Pending / In Progress / Completed
- **REST API** for task operations (JSON)
- Responsive dark-space UI with Bootstrap 5

---

## 🛠 Technologies Used

| Technology       | Purpose                          |
|------------------|----------------------------------|
| Python 3.10+     | Backend language                 |
| Flask            | Web framework                    |
| PostgreSQL       | Relational database              |
| Flask-SQLAlchemy | ORM (database interaction)       |
| Flask-Login      | User session management          |
| Werkzeug         | Password hashing                 |
| Bootstrap 5      | Frontend UI framework            |
| python-dotenv    | Environment variable management  |

---

## 📁 Folder Structure

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
│   │   ├── js/main.js       # Small UI helpers
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

## ⚙️ Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/taskorbit.git
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

## 🐘 PostgreSQL Setup

### 1. Create a database

```sql
CREATE DATABASE taskorbit_db;
```

### 2. Set up your `.env` file

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=pick-any-long-random-string-here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskorbit_db
```

> ⚠️ Never commit your `.env` file. It's already in `.gitignore`.

---

## ▶️ How to Run

```bash
python run.py
```

Open: **http://127.0.0.1:5000**

Database tables are created automatically on first run.

---

## 📋 Task Management Module

After logging in, users land on the **Dashboard** which shows:

- A welcome message with task summary
- 4 stat cards: Total / Pending / In Progress / Completed
- An overall progress bar
- A list of all tasks with priority and status badges
- Edit and Delete buttons per task
- Empty state when no tasks exist

### Task Fields

| Field        | Type    | Values                              |
|--------------|---------|-------------------------------------|
| Title        | String  | Required, max 200 chars             |
| Description  | Text    | Optional                            |
| Priority     | String  | Low / Medium / High                 |
| Status       | String  | Pending / In Progress / Completed   |
| Created Date | DateTime| Auto-generated                      |

---

## 🔌 REST API Endpoints

All API endpoints require the user to be logged in (session cookie).

### GET /api/tasks
Returns all tasks for the logged-in user.

**Response 200:**
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
Create a new task.

**Request body:**
```json
{
  "title": "Write unit tests",
  "description": "Cover all route handlers",
  "priority": "Medium",
  "status": "Pending"
}
```

**Response 201:** Returns the created task object.

---

### PUT /api/tasks/\<id\>
Update an existing task.

**Request body** (any fields you want to update):
```json
{
  "status": "Completed"
}
```

**Response 200:** Returns the updated task object.

**Response 403:** If the task belongs to another user.

---

### DELETE /api/tasks/\<id\>
Delete a task.

**Response 200:**
```json
{ "message": "Task deleted." }
```

**Response 403:** If the task belongs to another user.

---

## 📸 Screenshots

| Page       | Preview |
|------------|---------|
| Home       | ![Home](#) |
| Login      | ![Login](#) |
| Dashboard  | ![Dashboard](#) |
| Add Task   | ![Add Task](#) |

---

## 👨‍💻 Author

Built by **Nihar Ranjan Patra** — a student learning Flask.
Feel free to fork and build on top of it!

- GitHub: [Niharxd](https://github.com/Niharxd)
- LinkedIn: [nihar-patra-2277np](https://www.linkedin.com/in/nihar-patra-2277np/)
