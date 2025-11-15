# Specification: MindQuest CLI

## 1. Overview

MindQuest is a command line application in Python that merges a personal journal with a task manager called "Quests". It is designed to help users track their goals and their daily thoughts.

## 2. Core Featues

The application must be a single Python package that can be run from the command line. It will use a single **SQLite** database file, 'mindquest.db', to store all data.

### 2.1. Feature: Quests (Task Management)

- **Data:** The app must have a 'quests' table in the database.
  - 'id' (INTEGER, Primary Key, Autoincrement)
  - 'description' (TEXT)
  - 'status'(TEXT: 'active' or 'completed')
- **Commands:**
  - 'quest add <description>': Adds a new task to the 'quest' table with 'active' status.
  - 'quest list': Lists all 'active'  quests.
  - 'quest done <id>': Marks a quest as 'completed'.

### 2.2. Feature: Journal (Knowledge Management) 

- **Data:** The app must have a 'journal' table in the database.
  - 'id' (INTEGER, Primary Key, Autoincrement)
  - 'content' (TEXT)
  - 'created_at' (TIMESTAMP)
- **Commands:**  
  - 'journal add <content>': Adds a new journal entry.

## 3. Database

- The aaplication muse use the 'sqlite3' Python module.
- It must have a 'setup_database()' function that creates both the 'quests' and 'journal' tables if they do not exist.

## 4. Entry Point

- The application must have a 'main()' function that reads command line arguments using 'sys.argv' to run the correct functions e.g., 'quest add', 'journal add', etc.
