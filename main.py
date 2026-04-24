from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
""")
conn.commit()


# Request model
class Task(BaseModel):
    task: str


# Home
@app.get("/")
def home():
    return {"message": "Task API running with DB 🚀"}


# GET all tasks
@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    return [{"id": row[0], "task": row[1]} for row in rows]


# POST new task
@app.post("/tasks")
def add_task(task: Task):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task.task,))
    conn.commit()
    return {"message": "Task added", "task": task.task}


# DELETE task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": f"Task {task_id} deleted"}