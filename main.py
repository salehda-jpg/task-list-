from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = []
counter = 1


@app.get("/tasks")
def get_tasks(priority: int | None = None):
    """Return all tasks, or filter by priority."""
    if priority is not None:
        if priority < 1 or priority > 3:
            raise HTTPException(
                status_code=422,
                detail="Priority must be between 1 and 3"
            )
        return [task for task in tasks if task["priority"] == priority]

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
    """Add a task with a title, owner, and priority."""
    global counter

    priority = task.get("priority", 2)

    if not isinstance(priority, int) or priority < 1 or priority > 3:
        raise HTTPException(
            status_code=422,
            detail="Priority must be an integer between 1 and 3"
        )

    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
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
