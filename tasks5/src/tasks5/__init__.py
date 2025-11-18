import sys
import os
import sqlite3
Data_File = "tasks.db"
def setup_database():
    conn = sqlite3.connect(Data_File)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL)")
    conn.commit()
    conn.close()
def list_tasks():
    conn = sqlite3.connect(Data_File)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        print("You have no tasks.")
        return
    print ("-----Your Task-----")
    for task in tasks:
        print(f"{task[0]}. {task[1]}")
    print ("---------------")
def add_tasks(new_task_text):
    conn = sqlite3.connect(Data_File)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description) VALUES (?)", (new_task_text,))
    conn.commit()
    conn.close()
    print (f"New Task Added: '{new_task_text}'")
def search_tasks(search_term):
    conn = sqlite3.connect(Data_File)
    cursor = conn.cursor()
    search_query = f"%{search_term}%"
    cursor.execute("SELECT * FROM tasks WHERE description LIKE ?", (search_query,))
    tasks_found = cursor.fetchall()
    conn.close()
    if not tasks_found:
        print(f"No tasks found matching '{search_term}'")
    else:
        print(f"-----Search Results for '{search_term}'-----")
        for task in tasks_found:
            print(f"-{task[1]}")
        print("---------------")
def main():
    setup_database()
    if len(sys.argv) < 2:
        print("Welcome to Task Manager!")
        print("Usage:")
        print("  py tasks.py list     - Lists all tasks")
        print("  py tasks.py add <task>     - Adds a new task")
        print("  py tasks.py search <term>     - Searches for tasks")
    else:
        command = sys.argv[1]
        if command == "list":
            list_tasks()
        elif command == "add":
            new_task_text = ""
            for a in sys.argv[2:]:
                new_task_text = new_task_text + a + " "
            new_task_text = new_task_text.strip()
            if not new_task_text:
                print("Error: 'add' command needs text for the task.")
            else: 
                add_tasks(new_task_text)
        elif command == "search":
            search_term_text = ""
            for s in sys.argv[2:]:
                search_term_text = search_term_text + s + " "
            search_term_text = search_term_text.strip()
            if not search_term_text:
                print("Error: 'search' command needs a term to search for.")
            else:
                search_tasks(search_term_text)
        else:
            print(f"Error: Unknown command '{command}'")
if __name__ == "__main__":
    main()                        