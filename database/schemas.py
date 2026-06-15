"""
Database schema definitions for SQLite.
"""

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        grade INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS schedules (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        category TEXT,
        is_completed BOOLEAN DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        ai_feedback_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS feedback (
        id TEXT PRIMARY KEY,
        schedule_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        overall_score INTEGER,
        strengths TEXT,
        weaknesses TEXT,
        suggestions TEXT,
        summary TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (schedule_id) REFERENCES schedules (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS reminders (
        id TEXT PRIMARY KEY,
        schedule_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        reminder_time TEXT NOT NULL,
        is_sent BOOLEAN DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (schedule_id) REFERENCES schedules (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """,
]

# Index definitions for performance
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_schedules_user ON schedules(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_schedules_due_date ON schedules(due_date)",
    "CREATE INDEX IF NOT EXISTS idx_schedules_priority ON schedules(priority)",
    "CREATE INDEX IF NOT EXISTS idx_feedback_user ON feedback(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_reminders_user ON reminders(user_id)",
]
