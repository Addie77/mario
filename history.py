import sqlite3
import os

db_dir = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "sqlite.db")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time INTEGER NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
except Exception as e:
    print(f"資料表建立失敗：{e}")

def save_history(pass_time, score):
    db_path = os.path.join(os.path.dirname(__file__), "db", "sqlite.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (time, score) VALUES (?, ?)", (pass_time, score))
    conn.commit()
    conn.close()

def get_best_history():
    db_path = os.path.join(os.path.dirname(__file__), "db", "sqlite.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM history ORDER BY time ASC LIMIT 3")
    best_times = [str(r[0]) for r in cursor.fetchall()]
    cursor.execute("SELECT score FROM history ORDER BY score DESC LIMIT 3")
    best_scores = [str(r[0]) for r in cursor.fetchall()]
    conn.close()
    return best_times, best_scores

def clear_history():
    db_path = os.path.join(os.path.dirname(__file__), "db", "sqlite.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()