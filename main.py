from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(
    title="Task Manager API",
    description="Simple Task Manager using FastAPI",
    version="1.0.0"
)


# -----------------------------
# Task Status
# -----------------------------

class TaskStatus(str, Enum):
    pending = "Pending"
    completed = "Completed"


# -----------------------------
# Request Model
# -----------------------------

class TaskCreate(BaseModel):
    title: str


# -----------------------------
# Response Model
# -----------------------------

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus


# -----------------------------
# In-Memory Storage
# -----------------------------

tasks: list[Task] = []

next_id = 1


# -----------------------------
# 1. Welcome Endpoint
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Task Manager API"
    }


# -----------------------------
# 2. Add Task
# -----------------------------

@app.post("/tasks", response_model=Task)
def add_task(task_data: TaskCreate):

    global next_id

    new_task = Task(
        id=next_id,
        title=task_data.title,
        status=TaskStatus.pending
    )

    tasks.append(new_task)

    next_id += 1

    return new_task


# -----------------------------
# 3. View All Tasks
# -----------------------------

@app.get("/tasks", response_model=list[Task])
def get_tasks(
    status: TaskStatus | None = None
):

    if status is None:
        return tasks

    filtered_tasks = [
        task for task in tasks
        if task.status == status
    ]

    return filtered_tasks


# -----------------------------
# 4. Mark Task as Completed
# -----------------------------

@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):

    for task in tasks:

        if task.id == task_id:

            task.status = TaskStatus.completed

            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# -----------------------------
# 5. Delete Task
# -----------------------------

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            tasks.pop(index)

            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )