import sqlite3
import os

# 確保 db 資料夾存在
db_dir = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(db_dir, exist_ok=True)

db_path = os.path.join(db_dir, "sqlite.db")

try:
    conn = sqlite3.connect(db_path)
    print(f"成功打開資料庫：{db_path}")

    cursor = conn.cursor()
    # 建立 time 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time (
            id INTEGER PRIMARY KEY NOT NULL,
            time INTEGER NOT NULL
        )
    ''')
    # 建立 score 資料表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS score (
            id INTEGER PRIMARY KEY NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    print("資料表檢查/建立完成")
    conn.close()
except Exception as e:
    print(f"打開資料庫失敗：{e}")