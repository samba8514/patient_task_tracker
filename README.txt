# Patient Task Tracker

This project is a simple Flask-based application for tracking patient-related tasks. It demonstrates the following features:

- **Login System** with user roles (admin or regular).
- **Deadline Tracking** with color indicators (green for >7 days, yellow for <=7, red if overdue).
- **Task Update Logging** to record who completed a task and when.
- Basic HTML templates for listing and completing tasks.

To initialize the database, run the following commands:

```bash
python -c "from app import db; db.create_all()"
```

Run the development server:

```bash
flask run
```

Dependencies are listed in `requirements.txt`.
