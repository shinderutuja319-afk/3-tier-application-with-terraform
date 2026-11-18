import os
import time
import psycopg2

from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "cloudtask")
DB_USER = os.getenv("DB_USER", "clouduser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "localdevpassword")
DB_PORT = int(os.getenv("DB_PORT", "5432"))


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        connect_timeout=5
    )


def initialize_database():
    for attempt in range(10):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS tasks (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            completed BOOLEAN DEFAULT FALSE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
            return
        except psycopg2.OperationalError:
            if attempt == 9:
                raise
            time.sleep(3)


@app.route("/api/health", methods=["GET"])
def health():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    except psycopg2.Error:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, title, completed, created_at
                FROM tasks
                ORDER BY id DESC
            """)
            tasks = cur.fetchall()

    for task in tasks:
        task["created_at"] = task["created_at"].isoformat()

    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Task title is required"}), 400

    if len(title) > 255:
        return jsonify({"error": "Task title must be under 256 characters"}), 400

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO tasks (title)
                VALUES (%s)
                RETURNING id, title, completed, created_at
            """, (title,))
            task = cur.fetchone()

    task["created_at"] = task["created_at"].isoformat()
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}

    if not isinstance(data.get("completed"), bool):
        return jsonify({"error": "A boolean completed value is required"}), 400

    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                UPDATE tasks
                SET completed = %s
                WHERE id = %s
                RETURNING id, title, completed, created_at
            """, (data["completed"], task_id))

            task = cur.fetchone()

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    task["created_at"] = task["created_at"].isoformat()
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM tasks WHERE id = %s RETURNING id",
                (task_id,)
            )
            deleted = cur.fetchone()

    if deleted is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"})


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)