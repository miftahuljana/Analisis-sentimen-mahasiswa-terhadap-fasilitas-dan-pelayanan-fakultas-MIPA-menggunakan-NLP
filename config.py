import sqlite3

conn = sqlite3.connect(
    'database.db',
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS hasil_sentimen(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    komentar TEXT,
    preprocessing TEXT,
    sentimen TEXT
)
""")

conn.commit()