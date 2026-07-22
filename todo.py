
import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"


# ---------- Data handling ----------

def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file
    doesn't exist yet or is empty/corrupted."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks):
    """Save the current task list to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    """Work out the next available task ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


# ---------- Core features ----------

def add_task(tasks):
    title = input("Enter task: ").strip()
    if title == "":
        print("Task cannot be empty.")
        return

    new_task = {
        "id": get_next_id(tasks),
        "title": title,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully.")


def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\nAll Tasks:")
    print("-" * 60)
    for task in tasks:
        print(f"{task['id']:<4} | {task['title']:<25} | "
              f"{task['status']:<10} | {task['created_at']}")
    print("-" * 60)


def search_task(tasks):
    keyword = input("Enter keyword: ").strip().lower()
    results = [t for t in tasks if keyword in t["title"].lower()]

    if not results:
        print("No tasks found.")
        return

    print("\nSearch Results:")
    for task in results:
        print(f"{task['id']} | {task['title']} | {task['status']}")


def find_task_by_id(tasks, task_id):
    """Return the task dict with the given id, or None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def get_task_id_input():
    """Ask the user for a task ID and validate it's a number."""
    raw = input("Enter Task ID: ").strip()
    if not raw.isdigit():
        print("Please enter a valid numeric ID.")
        return None
    return int(raw)


def delete_task(tasks):
    task_id = get_task_id_input()
    if task_id is None:
        return

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print("Task not found.")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print("Task deleted.")


def update_status(tasks):
    task_id = get_task_id_input()
    if task_id is None:
        return

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print("Task not found.")
        return

    print("1. Pending\n2. Completed")
    choice = input("Select status: ").strip()

    if choice == "1":
        task["status"] = "Pending"
    elif choice == "2":
        task["status"] = "Completed"
    else:
        print("Invalid status choice.")
        return

    save_tasks(tasks)
    print("Status updated.")


def edit_task_title(tasks):
    task_id = get_task_id_input()
    if task_id is None:
        return

    task = find_task_by_id(tasks, task_id)
    if task is None:
        print("Task not found.")
        return

    new_title = input("Enter new title: ").strip()
    if new_title == "":
        print("Title cannot be empty.")
        return

    task["title"] = new_title
    save_tasks(tasks)
    print("Task updated.")


# ---------- Menu ----------

def print_menu():
    print("\n" + "=" * 40)
    print("        TO-DO LIST APP")
    print("=" * 40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Search Task")
    print("4. Delete Task")
    print("5. Update Task Status")
    print("6. Edit Task Title")
    print("7. Exit")
    print("=" * 40)


def main():
    tasks = load_tasks()

    menu_actions = {
        "1": add_task,
        "2": view_tasks,
        "3": search_task,
        "4": delete_task,
        "5": update_status,
        "6": edit_task_title,
    }

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "7":
            print("Goodbye!")
            break

        action = menu_actions.get(choice)
        if action:
            action(tasks)
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()