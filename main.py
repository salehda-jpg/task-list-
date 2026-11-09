from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = []
counter = 1


@app.get("/tasks")
def get_tasks():
    """Return all tasks."""
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Return one task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def add_task(task: dict):
    """Add a task with a title and an owner."""
    global counter

    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner")
    }

    tasks.append(new_task)
    counter += 1
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by its ID."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}

    raise HTTPException(status_code=404, detail="Task not found")
