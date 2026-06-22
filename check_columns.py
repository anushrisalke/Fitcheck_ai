import sqlite3

conn = sqlite3.connect("fitcheck.db")

cursor = conn.cursor()

cursor.execute(
    "PRAGMA table_info(analyses)"
)

print(cursor.fetchall())
