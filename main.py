from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "todo.db"


# =========================
# DATABASE
# =========================
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


# =========================
# ROUTES
# =========================
@app.route("/")
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    deadline = request.form.get("deadline")

    if title and deadline:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO tasks (title, deadline, done) VALUES (?, ?, ?)",
            (title, deadline, 0)
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    conn = get_db_connection()
    task = conn.execute("SELECT done FROM tasks WHERE id = ?", (task_id,)).fetchone()

    if task:
        new_done = 0 if task["done"] == 1 else 1
        conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (new_done, task_id))
        conn.commit()

    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


# =========================
# AUTO INIT DB (IMPORTANT)
# =========================
init_db()


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
