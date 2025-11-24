import sys
import os
import sqlite3
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
DB_FILE = "mindquest.db"
API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_sentiment(content: str):
    if not API_KEY:
        print("⚠️ AI ERROR: OPENAI_API_KEY environment variable not set. Skipping sentiment analysis.")
        return 0.0
    try:
        client = OpenAI(api_key=API_KEY)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the sentiment of the following journal entry. "
                    "Reply with *only* a single float number between -1.0 (most negative) "
                    "and +1.0 (most positive). Do not include any words, symbols or text."
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=0.0
        )
        raw_score = completion.choices[0].message.content.strip()
        return float(raw_score)
    except ValueError:
        print(f"⚠️ AI Parse Error: AI returned non-numeric data: '{raw_score}'. Defaulting to 0.0.")
        return 0.0
    except Exception as e:
        print(f"⚠️AI API Error: Could not get sentiment. {e}")
        return 0.0

def get_db_connection():
    return sqlite3.connect(DB_FILE)

def setup_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            sentiment_score REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS character (
            name TEXT,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0
        )
        """)
        cursor.execute("SELECT COUNT(*) FROM character")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO character (name) VALUES ('Adventurer')")
        
        conn.commit()

def get_status():
    """Retrieves the current character level and XP."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, level, xp FROM character LIMIT 1")
        status = cursor.fetchone()
    if status:
        name, level, xp = status
        xp_to_next = level * 100
        print(f"\n👤 --- Adventurer Status ---")
        print(f"   Name: {name}")
        print(f"   Level: {level}")
        print(f"   XP: {xp}/{xp_to_next}")
        print("---------------------------\n")
    else:
        print("Error: Character status not found.")

def grant_xp(conn, amount):
    XP_REWARD = amount
    cursor = conn.cursor()
    cursor.execute("UPDATE character SET xp = xp + ?", (XP_REWARD,))
    cursor.execute("SELECT level, xp FROM character LIMIT 1")
    level, xp = cursor.fetchone()
    xp_to_next = level * 100
    if xp >= xp_to_next:
        cursor.execute("UPDATE character SET level = level + 1, xp = xp - ?", (xp_to_next,)) 
        print(f"🎉 LEVEL UP! You are now Level {level + 1}!")

def add_quest(description):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quests (description) VALUES (?)", (description,))
        conn.commit()
    print(f"⚔️ New Quest Accepted: '{description}'")

def list_quests():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, description, status FROM quests WHERE status='active' ORDER BY id ASC")
        quests_list = cursor.fetchall()
    print("\n📜 --- Active Quests ---")
    if not quests_list:
        print("   No active quests. Time to explore!")
    else:
        for q in quests_list:
            print(f"   [{q[0]}] {q[1]}")
    print("------------------------\n")

def complete_quest(quest_id):
    try:
        quest_id = int(quest_id)
    except ValueError:
        print("Error: Quest ID must be a number.")
        return
    with get_db_connection() as conn: # Only one connection opened here
        cursor = conn.cursor()
        cursor.execute("UPDATE quests SET status='completed' WHERE id=?", (quest_id,))       
        if cursor.rowcount > 0:
            # Pass the existing connection (conn) to grant_xp
            grant_xp(conn, 50) 
            print(f"✨ Quest {quest_id} Complete! +50 XP!")
        else:
            print(f"⚠️ Quest ID {quest_id} not found or already completed.")    
        conn.commit()

def add_journal_entry(content):
    sentiment_score = analyze_sentiment(content)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO journal (content, sentiment_score) VALUES (?, ?)", (content, sentiment_score))
        conn.commit()
    print(f"✍️ Journal Entry Logged. Sentiment: {sentiment_score:.2f}")

def list_journal():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, created_at, content, sentiment_score FROM journal ORDER BY id DESC LIMIT 5")
        entries = cursor.fetchall()
    print("\n📖 --- Recent Journal Entries ---")
    if not entries:
        print("   The pages are blank.")
    else:
        for e in entries:
            date_time = datetime.strptime(e[1].split('.')[0], '%Y-%m-%d %H:%M:%S').strftime('%b %d, %I:%M%p')
            content_snippet = e[2][:40] + ('...' if len(e[2]) > 40 else '')
            sentiment_tag = ""
            if e[3] > 0.5: sentiment_tag = "😊"
            elif e[3] < -0.5 : sentiment_tag = "😞"
            else: sentiment_tag = "😐"
            print(f"   [{sentiment_tag} {e[3]:.2f}] [{date_time}] {content_snippet}")
    print("---------------------------------\n")

def remove_journal_entry(entry_id):
    try:
        entry_id = int(entry_id)
    except ValueError:
        print("Error: Journal ID must be a number.")
        return
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM journal WHERE id=?", (entry_id,))
        if cursor.rowcount == 0:
            print(f"⚠️ Error: Journal entry ID {entry_id} not found.")
        else:
            print(f"🗑️ Journal Entry {entry_id} permanently removed.")
        
        conn.commit()

def display_mood_board():
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT created_at, sentiment_score FROM journal
        WHERE created_at >= ?
        ORDER BY created_at DESC
        """, (seven_days_ago,))
        entries = cursor.fetchall()
        if entries:
            total_score = sum(e[1] for e in entries)
            avg_score = total_score / len(entries)
        else:
            print("\n📊 ---Mood Board---")
            print("   Not enough data (less than 7 days of entries).")
            print("-----------------\n")
            return
    if avg_score > 0.5:
        emoji = "😄"
        message = "High Productivity Zone."
    elif avg_score < -0.5:
        emoji = "😭"
        message = "Critical Stress Warning"
    else:
        emoji = "😐"
        message = "Stable and Balanced"
    print("\n📊 --- Last 7 Day Mood Board ---")
    print(f"   Overall Vibe: {emoji} {message}")
    print(f"   Average Sentiment: {avg_score:.2f}")
    print(f"   Total Entries: {len(entries)}")
    print("--------------------\n")

def main():
    setup_database()
    if len(sys.argv) < 2:
        print("\n--- MindQuest: The AI-Powered Journal & RPG ---\n")
        print("Usage:")
        print("  mindquest status               - View character status (XP/Level)")
        print("  mindquest mood-board           - View 7-day average sentiment report")
        print("  mindquest quest add <text>     - Add a new task/quest")
        print("  mindquest quest list           - See active quests")
        print("  mindquest quest done <id>      - Complete a quest")
        print("  mindquest journal add <text>   - Write a journal entry")
        print("  mindquest journal list         - Read recent entries")
        print("  mindquest journal remove <id>  - Remove an entry permanently")
        return
    category = sys.argv[1] 
    if category == "status":
        get_status()
        return
    elif category == "mood-board":
        display_mood_board()
        return
    if len(sys.argv) < 3:
        print(f"Error: Missing command for '{category}'. Try 'list' or 'add'.")
        return
    command = sys.argv[2]
    text = " ".join(sys.argv[3:]).strip() 
    if category == "quest":
        if command == "list":
            list_quests()
        elif command == "add":
            if text: add_quest(text)
            else: print("Error: Quest description required.")
        elif command == "done":
            if text: 
                complete_quest(text)
            else: 
                print("Error: Quest ID required.")
    elif category == "journal":
        if command == "list":
            list_journal()
        elif command == "add":
            if text: add_journal_entry(text)
            else: print("Error: Journal content required.")
        elif command == "remove":
            if text:
                remove_journal_entry(text)
            else:
                print("Error: Journal entry ID required.")
    else:
        print(f"Error: Unknown category '{category}'. Use 'quest', 'journal', or 'status'.")