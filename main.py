from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def get_connection():
    return sqlite3.connect("tasks.db")

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    completed: bool

@app.get("/")
def home():
    return {"message": "Task manager API is running"}

@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, title, completed FROM tasks")
    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "completed": bool(row[2])
        }
        for row in rows
    ]

@app.get("/tasks/{task_id}")
def find_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
            "id": row[0],
            "title": row[1],
            "completed": bool(row[2])
    }


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    connection = get_connection()
    cursor = connection.cursor()
        
    cursor.execute(
        """INSERT INTO tasks (title, completed)
        VALUES (?, ?)
        """,
        (task_data.title, 0)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()
    
    return {
            "id": task_id,
            "title": task_data.title,
            "completed": False
    }

@app.patch("/tasks/{task_id}")
def complete_task(task_id: int, task_data: TaskUpdate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE tasks
    SET completed = ?
    WHERE id = ?
    """,
    (int(task_data.completed), task_id)
    )

    connection.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute("SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,))
    
    row = cursor.fetchone()
    
    connection.close()

    return {
        "id": row[0],
        "title": row[1],
        "completed": bool(row[2])
    }

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE id = ?
    """
    (task_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

    connection.close()

    return {"message": "Task deleted"}