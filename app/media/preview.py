import os
import subprocess
import math
from app.core.config import get_folders
from database.db import set_preview_paths


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def generate_thumbnail(input_path, output_dir, timestamp=3, width=320):
    _ensure_dir(output_dir)
    base = os.path.splitext(os.path.basename(input_path))[0]
    out = os.path.join(output_dir, f"{base}_thumb.jpg")
    # Use ffmpeg to grab a frame at `timestamp` seconds
    cmd = [
        'ffmpeg', '-y', '-ss', str(timestamp), '-i', input_path,
        '-frames:v', '1', '-q:v', '2', '-vf', f'scale={width}:-1', out
    ]
    subprocess.run(cmd, check=False)
    return out if os.path.exists(out) else None


def generate_preview(input_path, output_dir, start=2, duration=3, width=480):
    _ensure_dir(output_dir)
    base = os.path.splitext(os.path.basename(input_path))[0]
    out = os.path.join(output_dir, f"{base}_preview.mp4")
    cmd = [
        'ffmpeg', '-y', '-ss', str(start), '-i', input_path,
        '-t', str(duration), '-c:v', 'libx264', '-crf', '28',
        '-preset', 'veryfast', '-vf', f'scale={width}:-2',
        '-c:a', 'aac', '-b:a', '64k', out
    ]
    subprocess.run(cmd, check=False)
    return out if os.path.exists(out) else None


def _choose_timestamps(duration):
    if not duration or duration < 1:
        return (0, 0)
    t = min(3, max(0, math.floor(duration / 4)))
    return (t, max(1, min(3, int(duration - t))))


def generate_and_store(input_path, video_id):
    folders = get_folders()
    temp = folders.get('temp') or os.path.join(os.getcwd(), 'temp')
    thumbs_dir = os.path.join(temp, 'thumbnails')
    previews_dir = os.path.join(temp, 'previews')
    # Try to probe duration via ffprobe (best-effort)
    duration = None
    try:
        import subprocess
        res = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', input_path
        ], capture_output=True, text=True)
        duration = float(res.stdout.strip()) if res.stdout.strip() else None
    except Exception:
        duration = None

    thumb_ts, preview_dur = _choose_timestamps(duration)
    thumb = generate_thumbnail(input_path, thumbs_dir, timestamp=thumb_ts)
    preview = generate_preview(input_path, previews_dir, start=thumb_ts, duration=preview_dur)

    # Store in DB (paths may be absolute)
    try:
        set_preview_paths(video_id, thumb, preview)
    except Exception:
        pass

    return thumb, preview
