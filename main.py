from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# In-memory storage (temporary)
tasks = []

# Model (this defines the structure of your data)
class Task(BaseModel):
    task: str

@app.get("/")
def home():
    return {"message": "Task API running"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task.dict())
    return {"message": "Task added", "tasks": tasks}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id < len(tasks):
        tasks.pop(task_id)
        return {"message": "Task deleted"}
    return {"error": "Invalid ID"}