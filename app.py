from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI(title="TaskFlow - Minimal Task Manager API")

# Database setup
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            done BOOLEAN DEFAULT 0
        )"""
    )
    conn.commit()
    conn.close()

init_db()

# Model
class Task(BaseModel):
    title: str
    description: str = ""
    done: bool = False

# Routes
@app.get("/")
def home():
    return {"message": "Welcome to TaskFlow API 🚀"}

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)",
                   (task.title, task.description, task.done))
    conn.commit()
    conn.close()
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [Task(title=row[0], description=row[1], done=bool(row[2])) for row in rows]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted"}
