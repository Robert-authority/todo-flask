from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Lokasi database (Railway aman)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "todo.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT,
            is_done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    # PENTING: pastikan tabel selalu ada
    init_db()

    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    init_db()

    title = request.form.get("title")
    deadline = request.form.get("deadline")

    if title:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO tasks (title, deadline, is_done) VALUES (?, ?, 0)",
            (title, deadline)
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    init_db()

    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if task:
        new_status = 0 if task["is_done"] == 1 else 1
        conn.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (new_status, task_id))
        conn.commit()

    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    init_db()

    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
