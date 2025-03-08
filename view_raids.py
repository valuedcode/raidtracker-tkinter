import sqlite3

# ✅ Connect to the database
conn = sqlite3.connect("tarkov_raids.db")
cursor = conn.cursor()

# ✅ Fetch all stored raids
cursor.execute("SELECT * FROM raids")
raids = cursor.fetchall()

conn.close()

# ✅ Print stored data
print("\n🔹 Logged Raids:")
for raid in raids:
    print(raid)

if not raids:
    print("No raids found in the database.")
