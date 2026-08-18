import os
import glob
import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database.db import (get_all_videos, get_video_by_id, update_status,
                          reset_stuck_jobs, add_video, delete_completed,
                          update_progress, delete_video, delete_by_filepath)
from app.media.metadata import extract_metadata
from app.workflow.orchestrator import process_video
from app.core.config import load_config, get_folders, get_file_manager
from app.export.naming import get_next_version_label

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith(('.mp4', '.mov')):
            print(f"Watcher detected: {event.src_path}")
            metadata = extract_metadata(event.src_path)
            add_video(event.src_path, metadata)

    def on_deleted(self, event):
        if event.src_path.lower().endswith(('.mp4', '.mov')):
            print(f"Watcher noticed deletion: {event.src_path}")
            delete_by_filepath(event.src_path)

def start_watcher():
    folders = get_folders()
    raw_folder = folders['raw_videos']
    observer = Observer()
    observer.schedule(VideoHandler(), raw_folder, recursive=True)
    observer.start()
    print(f"Watcher started: {raw_folder}")
    try:
        while True:
            time.sleep(2)
    except Exception:
        observer.stop()
    observer.join()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SME starting up — checking for stuck jobs...")
    reset_stuck_jobs()
    watcher_thread = threading.Thread(target=start_watcher, daemon=True)
    watcher_thread.start()
    yield
    print("SME shutting down.")

app = FastAPI(title="SME Local API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/videos")
def list_videos():
    rows = get_all_videos()
    return [
        {
            "id": r[0],
            "filepath": r[1],
            "programme": r[2],
            "week": r[3],
            "module": r[4],
            "lesson_number": r[5],
            "lesson_title": r[6],
            "status": r[7],
            "date_added": r[8],
            "progress": r[9],
            "srt_path": r[10]
        }
        for r in rows
    ]

@app.get("/config")
def get_config():
    return load_config()

@app.post("/config")
def save_config(data: dict):
    import json
    config_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'config', 'settings.json'
    )
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    return {"status": "saved"}

@app.post("/open-folder/{folder_key}")
def open_folder(folder_key: str):
    import subprocess
    folders = get_folders()
    file_manager = get_file_manager()
    path = folders.get(folder_key)
    if not path:
        return {"error": "Unknown folder key"}
    subprocess.Popen([file_manager, path])
    return {"status": "opened"}

@app.get("/next-version/{video_id}")
def next_version(video_id: int):
    video = get_video_by_id(video_id)
    if not video:
        return {"label": "will create (Edited).mp4"}
    folders = get_folders()
    label = get_next_version_label(video[1], folders['edited_videos'])
    return {"label": label}

@app.post("/process/{video_id}")
def trigger_process(video_id: int):
    video = get_video_by_id(video_id)
    if not video:
        return {"error": "Video not found"}
    if not os.path.exists(video[1]):
        update_status(video_id, "failed")
        update_progress(video_id, "Source file not found on disk.")
        return {"error": f"File not found on disk: {video[1]}"}
    update_status(video_id, "processing")
    update_progress(video_id, "Starting…")
    try:
        from app.workflow.orchestrator import process_phase1
        result = process_phase1(video[1], video_id=video_id)
        if result == 'awaiting_review':
            update_status(video_id, "awaiting_review")
            return {"status": "awaiting_review"}
        update_status(video_id, "completed")
        update_progress(video_id, None)
        return {"status": "completed", "output": result}
    except Exception as e:
        update_status(video_id, "failed")
        update_progress(video_id, f"Error: {str(e)}")
        print(f"Processing failed for video {video_id}: {str(e)}")
        return {"status": "failed", "error": str(e)}

@app.get("/srt/{video_id}")
def get_srt(video_id: int):
    from database.db import get_srt_path
    srt_path = get_srt_path(video_id)
    if not srt_path or not os.path.exists(srt_path):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="SRT not found")
    with open(srt_path, 'r', encoding='utf-8') as f:
        return {"srt": f.read(), "path": srt_path}

@app.post("/srt/{video_id}")
def save_srt(video_id: int, data: dict):
    from database.db import get_srt_path
    srt_path = get_srt_path(video_id)
    if not srt_path:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="SRT path not found")
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(data['srt'])
    return {"status": "saved"}

@app.post("/approve/{video_id}")
def approve_and_render(video_id: int):
    video = get_video_by_id(video_id)
    if not video:
        return {"error": "Video not found"}
    from database.db import get_srt_path
    srt_path = get_srt_path(video_id)
    if not srt_path or not os.path.exists(srt_path):
        return {"error": "SRT file not found — re-process this video"}
    update_status(video_id, "processing")
    update_progress(video_id, "Rendering approved subtitles…")
    # Get any custom style saved from the editor
    custom_style = _render_styles.pop(video_id, None)
    try:
        from app.workflow.orchestrator import process_phase2
        output = process_phase2(video[1], srt_path, video_id=video_id,
                                caption_style=custom_style)
        update_status(video_id, "completed")
        update_progress(video_id, None)
        return {"status": "completed", "output": output}
    except Exception as e:
        update_status(video_id, "failed")
        update_progress(video_id, f"Error: {str(e)}")
        return {"status": "failed", "error": str(e)}

@app.post("/sync")
def sync_videos():
    folders = get_folders()
    edited_folder = folders['edited_videos']
    rows = get_all_videos()
    changes = []
    for r in rows:
        video_id = r[0]
        raw_path = r[1]
        status = r[7]

        # Never touch a job that is mid-pipeline
        if status in ('processing', 'awaiting_review'):
            continue

        if not os.path.exists(raw_path):
            delete_video(video_id)
            changes.append(f"Removed missing raw: {raw_path}")
            continue

        base = os.path.splitext(os.path.basename(raw_path))[0]
        pattern = os.path.join(edited_folder, f"{base} (Edited*).mp4")
        existing = glob.glob(pattern)

        if existing and status != 'completed':
            update_status(video_id, 'completed')
            update_progress(video_id, None)
            changes.append(f"Marked completed: {raw_path}")
        elif not existing and status == 'completed':
            update_status(video_id, 'detected')
            update_progress(video_id, None)
            changes.append(f"Reverted to detected: {raw_path}")

    return {"synced": True, "changes": changes}

@app.delete("/videos/completed")
def clear_completed():
    delete_completed()
    return {"status": "cleared"}

@app.get("/pick-folder")
def pick_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder = filedialog.askdirectory(title="Select Folder")
        root.destroy()
        if folder:
            return {"path": folder}
        return {"path": None}
    except Exception as e:
        return {"error": str(e)}

@app.get("/video-file/{video_id}")
def serve_video(video_id: int):
    from fastapi.responses import FileResponse
    video = get_video_by_id(video_id)
    if not video or not os.path.exists(video[1]):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(video[1], media_type="video/mp4")

@app.get("/edited-file/{video_id}")
def serve_edited(video_id: int):
    from fastapi.responses import FileResponse
    from fastapi import HTTPException
    import re
    video = get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    folders = get_folders()
    base = os.path.splitext(os.path.basename(video[1]))[0]
    pattern = os.path.join(folders['edited_videos'], f"{base} (Edited*).mp4")
    existing = glob.glob(pattern)
    if not existing:
        raise HTTPException(status_code=404, detail="No edited version found")

    def version_key(path):
        match = re.search(r'\(Edited v?(\d+)\)', path)
        return int(match.group(1)) if match else 0

    latest = sorted(existing, key=version_key)[-1]
    return FileResponse(latest, media_type="video/mp4")

@app.post("/restart")
def restart_server():
    import sys
    import subprocess
    import threading
    def do_restart():
        time.sleep(1)
        subprocess.Popen([sys.executable, "-m", "uvicorn",
                         "app.core.main:app", "--reload"],
                        cwd=os.path.dirname(
                            os.path.dirname(os.path.dirname(__file__))
                        ))
        os._exit(0)
    threading.Thread(target=do_restart, daemon=True).start()
    return {"status": "restarting"}

@app.post("/open-video")
def open_video_external(data: dict):
    import subprocess
    path = data.get("path")
    player = data.get("player", "default")
    if not path or not os.path.exists(path):
        return {"error": "File not found"}
    if player == "vlc":
        subprocess.Popen(["vlc", path])
    elif player == "mpv":
        subprocess.Popen(["mpv", path])
    elif player == "default":
        subprocess.Popen(["xdg-open", path])
    else:
        subprocess.Popen(["xdg-open", path])
    return {"status": "opened"}

@app.get("/raw-path/{video_id}")
def get_raw_path(video_id: int):
    video = get_video_by_id(video_id)
    if not video:
        return {"path": None}
    return {
        "path": video[1],
        "filename": os.path.basename(video[1])
    }

@app.get("/edited-path/{video_id}")
def get_edited_path(video_id: int):
    import re
    video = get_video_by_id(video_id)
    if not video:
        return {"path": None}
    folders = get_folders()
    base = os.path.splitext(os.path.basename(video[1]))[0]
    pattern = os.path.join(folders['edited_videos'], f"{base} (Edited*).mp4")
    existing = glob.glob(pattern)
    if not existing:
        return {"path": None}

    def version_key(path):
        match = re.search(r'\(Edited v?(\d+)\)', path)
        return int(match.group(1)) if match else 0

    latest = sorted(existing, key=version_key)[-1]
    return {"path": latest, "filename": os.path.basename(latest)}

@app.post("/caption-style/{video_type}")
def save_caption_style(video_type: str, style: dict):
    import json
    if video_type not in ('lesson', 'reel', 'testimonial'):
        return {"error": "Invalid video type"}
    config_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'config', 'settings.json'
    )
    cfg = load_config()
    if 'lesson' not in cfg['captions']:
        # Migrate old flat format
        old = cfg['captions']
        cfg['captions'] = {
            'lesson': old.copy(),
            'reel': old.copy(),
            'testimonial': old.copy()
        }
    cfg['captions'][video_type] = style
    with open(config_path, 'w') as f:
        json.dump(cfg, f, indent=2)
    return {"status": "saved"}

@app.get("/caption-style/{video_id}")
def get_video_caption_style(video_id: int):
    from app.core.config import get_caption_style
    from app.workflow.orchestrator import get_template
    video = get_video_by_id(video_id)
    if not video:
        return get_caption_style('lesson')
    template = get_template(video[1])
    return get_caption_style(template)

# In-memory store for per-render caption styles
_render_styles = {}

@app.post("/srt-style/{video_id}")
def save_render_style(video_id: int, style: dict):
    _render_styles[video_id] = style
    return {"status": "saved"}

@app.get("/srt-style/{video_id}")
def get_render_style(video_id: int):
    return _render_styles.get(video_id, {})