# 🪐 TaskOrbit

> **Stay in orbit, stay productive.**

TaskOrbit is a real-time task management and productivity tracking web application built with Flask and PostgreSQL. It's designed to help you organize your tasks, track your progress, and stay focused — all in one clean, minimal interface.

---

## ✅ Features (Completed So Far)

- User Registration with validation
- Secure Login / Logout
- Password hashing (no plain-text passwords stored)
- Flash messages for feedback
- Protected routes (login required)
- Responsive dark-blue UI with Bootstrap 5
- Clean landing page with hero section and features

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
│   │   └── auth.py          # Login, Register, Logout routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User database model
│   ├── templates/
│   │   ├── base.html        # Base layout (navbar + footer)
│   │   ├── home.html        # Landing page
│   │   ├── login.html       # Login page
│   │   └── register.html    # Registration page
│   ├── static/
│   │   ├── css/style.css    # Custom dark-blue theme
│   │   ├── js/main.js       # Small UI helpers
│   │   └── images/          # (for future images)
│   ├── services/            # Business logic (future use)
│   └── __init__.py          # App factory
│
├── instance/                # Local config (not committed)
├── requirements.txt
├── run.py                   # Entry point
├── .env.example             # Environment variable template
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

### 1. Install PostgreSQL
Download from: https://www.postgresql.org/download/

### 2. Create a database

Open your terminal or pgAdmin and run:

```sql
CREATE DATABASE taskorbit_db;
```

### 3. Note your credentials
You'll need:
- PostgreSQL username (default: `postgres`)
- PostgreSQL password
- Database name: `taskorbit_db`

---

## 🔐 Environment Variable Setup

### 1. Copy the example file

```bash
cp .env.example .env
```

### 2. Edit `.env` with your actual values

```env
SECRET_KEY=pick-any-long-random-string-here
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/taskorbit_db
```

> ⚠️ Never commit your `.env` file to GitHub. It's already in `.gitignore`.

---

## ▶️ How to Run the Project

```bash
python run.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

The database tables will be created automatically on first run.

---

## 📸 Screenshots

> *(Add screenshots here once the app is running)*

| Page       | Preview |
|------------|---------|
| Home       | ![Home](#) |
| Login      | ![Login](#) |
| Register   | ![Register](#) |

---

## 🚀 Future Plans

- [ ] Task creation, editing, and deletion
- [ ] Task categories and priority levels
- [ ] Due dates and reminders
- [ ] Productivity dashboard with stats
- [ ] Dark/light mode toggle
- [ ] User profile page
- [ ] Search and filter tasks

---

## 👨‍💻 Author

Built by a student learning Flask — feel free to fork and build on top of it!
