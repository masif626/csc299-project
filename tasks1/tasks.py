import json
import sys
import os
Data_File = "tasks.json"
def load_tasks():
    if os.path.exists(Data_File):
        with open(Data_File, "r") as m:
            tasks = json.load(m)
            return tasks
    else:
        return []
def save_tasks(tasks):
    with open(Data_File, "w") as m:
        json.dump(tasks, m, indent=4)
def list_tasks(tasks):
    if not tasks:
        print("You have no tasks.")
        return
    print("-----Your Task-----")
    task_number = 1
    for t in tasks:
        print(f"{task_number}. {t}")
        task_number = task_number + 1
    print("---------------")
def add_tasks(tasks, new_tasks):
    tasks.append(new_tasks)
    save_tasks(tasks)
    print(f"New Task Added: '{new_tasks}'")
def search_tasks(tasks, search_term):
    tasks_found = []
    for t in tasks:
        if search_term.lower() in t.lower():
            tasks_found.append(t)
    if not tasks_found:
        print(f"No tasks found matching '{search_term}'")
    else:
        print(f"-----Search Results for '{search_term}'-----")
        for t in tasks_found:
            print(f"-{t}")
        print("---------------")
def main():
    tasks = load_tasks()
    if len(sys.argv) < 2:
        print("Welcome to Task Manager!")
        print("Usage:")
        print("   python tasks.py list    - Lists all tasks")
        print("   python tasks.py add <task>    - Adds a new task")
        print("   python tasks.py search <term>    - Search for tasks")
    else:
        command = sys.argv[1]
        if command == "list":
            list_tasks(tasks)
        elif command == "add":
            new_task_text = ""
            for a in sys.argv[2:]:
                new_task_text = new_task_text + a + " "
            new_task_text = new_task_text.strip()
            if not new_task_text:
                print("Error: 'add' command needs text for the task.")
            else:
                add_tasks(tasks, new_task_text)
        elif command == "search":
            search_term_text = ""
            for s in sys.argv[2:]:
                search_term_text = search_term_text + s + " "
            search_term_text = search_term_text.strip()
            if not search_term_text:
                print("Error: 'search' command needs a term to search for.")
            else:
                search_tasks(tasks, search_term_text)
        else:
            print(f"Error: Unknown command '{command}'")
if __name__ == "__main__":
    main()
