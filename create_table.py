import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("tarkov_raids.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS raids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        map_name TEXT NOT NULL,
        survived TEXT NOT NULL,
        kills INTEGER NOT NULL,
        xp INTEGER NOT NULL,
        time_spent INTEGER NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

# Save & close
conn.commit()
conn.close()

print("Database & table set up successfully!")
