import sqlite3
import os

os.makedirs("database", exist_ok=True)
DB_PATH = "database/sme.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filepath TEXT UNIQUE,
            programme TEXT,
            week TEXT,
            module TEXT,
            lesson_number TEXT,
            lesson_title TEXT,
            status TEXT DEFAULT 'detected',
            date_added TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_video(filepath, metadata):
    import glob
    from app.core.config import get_folders
    edited_folder = get_folders()['edited_videos']
    base = os.path.splitext(os.path.basename(filepath))[0]
    pattern = os.path.join(edited_folder, f"{base} (Edited*).mp4")
    existing_output = glob.glob(pattern)
    status = 'completed' if existing_output else 'detected'

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """INSERT OR IGNORE INTO videos
           (filepath, programme, week, module, lesson_number, lesson_title, status)
           VALUES (?,?,?,?,?,?,?)""",
        (filepath, metadata.get('programme'), metadata.get('week'),
         metadata.get('module'), metadata.get('lesson_number'),
         metadata.get('lesson_title'), status)
    )
    conn.commit()
    conn.close()

def get_all_videos():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, filepath, programme, week, module, lesson_number, "
        "lesson_title, status, date_added, progress, srt_path "
        "FROM videos ORDER BY date_added DESC"
    ).fetchall()
    conn.close()
    return rows

def get_video_by_id(video_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT * FROM videos WHERE id = ?", (video_id,)).fetchone()
    conn.close()
    return row

def update_status(video_id, status):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE videos SET status = ? WHERE id = ?", (status, video_id))
    conn.commit()
    conn.close()

def reset_stuck_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE videos SET status = 'detected' WHERE status = 'processing'")
    conn.commit()
    conn.close()
    print("Recovered any stuck jobs.")

def delete_completed():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM videos WHERE status = 'completed'")
    conn.commit()
    conn.close()
    print("Cleared completed jobs.")

def delete_video(video_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

def update_progress(video_id, progress_text):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE videos SET progress = ? WHERE id = ?", (progress_text, video_id))
    conn.commit()
    conn.close()

def delete_by_filepath(filepath):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM videos WHERE filepath = ?", (filepath,))
    conn.commit()
    conn.close()

def set_srt_path(video_id, srt_path):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE videos SET srt_path = ? WHERE id = ?",
                 (srt_path, video_id))
    conn.commit()
    conn.close()

def get_srt_path(video_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT srt_path FROM videos WHERE id = ?",
                       (video_id,)).fetchone()
    conn.close()
    return row[0] if row else None