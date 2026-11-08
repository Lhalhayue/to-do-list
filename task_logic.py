"""
Task operations and JSON data storage for PinkPlan.
This file does not create any GUI widgets.
"""

import json
from pathlib import Path

# Store tasks.json beside this Python file so the path works from any folder.
DATA_FILE = Path(__file__).resolve().parent / "tasks.json"


def load_tasks():
    """Read saved task records. Return an empty list if no valid data exists."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Write the current task list to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def add_task(tasks, title, priority, category, due_date):
    """Create a task, add it to the list and save the list."""
    task = {
        "title": title,
        "priority": priority,
        "category": category,
        "due_date": due_date,
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)


def update_task(tasks, index, title, priority, category, due_date):
    """Update the details of the task at the given list position."""
    if 0 <= index < len(tasks):
        tasks[index].update({
            "title": title,
            "priority": priority,
            "category": category,
            "due_date": due_date
        })
        save_tasks(tasks)


def delete_task(tasks, index):
    """Remove a task at the given list position."""
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)


def set_task_completed(tasks, index, completed=True):
    """Change the completion status of a task."""
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = completed
        save_tasks(tasks)


def get_visible_task_indices(tasks, keyword="", status="All Tasks", hide_completed=False):
    """Return original task positions that match the search and filter controls."""
    visible = []
    keyword = keyword.casefold().strip()

    for index, task in enumerate(tasks):
        matches_search = keyword in task["title"].casefold()
        matches_status = (
            status == "All Tasks"
            or (status == "Pending" and not task["completed"])
            or (status == "Completed" and task["completed"])
        )
        matches_checkbox = not hide_completed or not task["completed"]

        if matches_search and matches_status and matches_checkbox:
            visible.append(index)

    return visible
