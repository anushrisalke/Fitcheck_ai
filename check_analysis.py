import sqlite3

conn = sqlite3.connect("fitcheck.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM analyses"
)

print(cursor.fetchall())