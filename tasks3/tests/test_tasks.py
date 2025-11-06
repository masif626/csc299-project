import os
import sqlite3
from tasks3 import setup_database, add_tasks, get_tasks
Test_DB = "test_tasks.db"
import tasks3
tasks3.Data_File = Test_DB
def setup_function():
    if os.path.exists(Test_DB):
        os.remove(Test_DB)
    setup_database()
def test_add_and_get_tasks():
    setup_function()
    add_tasks("Test task 1")
    tasks = get_tasks()
    assert len(tasks) == 1
    assert tasks[0][1] == "Test task 1"
def test_get_empty_tasks():
    setup_function()
    tasks = get_tasks()
    assert len(tasks) == 0    