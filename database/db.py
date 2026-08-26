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
            date_added TEXT DEFAULT CURRENT_TIMESTAMP,
            progress TEXT,
            srt_path TEXT,
            duration REAL
        )
    ''')
    # Ensure older DBs have the newer columns
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(videos)")
    cols = [r[1] for r in cur.fetchall()]
    if 'progress' not in cols:
        conn.execute("ALTER TABLE videos ADD COLUMN progress TEXT")
    if 'srt_path' not in cols:
        conn.execute("ALTER TABLE videos ADD COLUMN srt_path TEXT")
    if 'duration' not in cols:
        conn.execute("ALTER TABLE videos ADD COLUMN duration REAL")
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

    # Update duration for this file (compute once at add-time)
    try:
        from app.media.render import get_video_duration
        row = conn.execute("SELECT id FROM videos WHERE filepath = ?", (filepath,)).fetchone()
        if row:
            vid = row[0]
            dur = get_video_duration(filepath)
            if dur is not None:
                conn.execute("UPDATE videos SET duration = ? WHERE id = ?", (dur, vid))
                conn.commit()
    except Exception:
        # Non-fatal: if probing fails, leave duration NULL
        pass

    conn.close()

def get_all_videos():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, filepath, programme, week, module, lesson_number, "
        "lesson_title, status, date_added, progress, srt_path, duration "
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


def backfill_durations(progress_callback=None):
    """Compute and store duration for videos that have NULL duration.

    progress_callback(optional): called with (processed, total) to report progress.
    """
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, filepath FROM videos WHERE duration IS NULL").fetchall()
    total = len(rows)
    processed = 0
    try:
        from app.media.render import get_video_duration
        for r in rows:
            vid, path = r[0], r[1]
            try:
                if path and os.path.exists(path):
                    dur = get_video_duration(path)
                    if dur is not None:
                        conn.execute("UPDATE videos SET duration = ? WHERE id = ?", (dur, vid))
                        conn.commit()
            except Exception:
                pass
            processed += 1
            if progress_callback:
                progress_callback(processed, total)
    finally:
        conn.close()