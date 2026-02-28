import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.cli_manager.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT UNIQUE NOT NULL,
            frequency INTEGER DEFAULT 1,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def upsert_command(command_text):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if command exists
    c.execute("SELECT id, frequency FROM commands WHERE command = ?", (command_text,))
    row = c.fetchone()
    
    now = datetime.now()
    
    if row:
        # Update existing
        new_freq = row['frequency'] + 1
        c.execute("UPDATE commands SET frequency = ?, last_used = ? WHERE id = ?", 
                  (new_freq, now, row['id']))
    else:
        # Insert new
        c.execute("INSERT INTO commands (command, frequency, last_used) VALUES (?, 1, ?)", 
                  (command_text, now))
    
    conn.commit()
    conn.close()

def get_all_commands(sort_by="last_used"):
    conn = get_db_connection()
    c = conn.cursor()
    
    if sort_by == "frequency":
        order = "frequency DESC, last_used DESC"
    else:
        order = "last_used DESC"
        
    c.execute(f"SELECT * FROM commands ORDER BY {order}")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
