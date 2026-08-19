import subprocess
import os
import re
import threading
from app.core.config import get_caption_style

def get_video_duration(video_path):
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ], capture_output=True, text=True)
    try:
        return float(result.stdout.strip())
    except:
        return None

def _run_ffmpeg_with_progress(cmd, duration, progress_callback):
    """Run an FFmpeg command and call progress_callback(pct) as it runs."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    for line in process.stderr:
        if progress_callback and duration:
            match = re.search(r'time=(\d+):(\d+):([\d.]+)', line)
            if match:
                h, m, s = match.groups()
                elapsed = int(h)*3600 + int(m)*60 + float(s)
                pct = min(99, int((elapsed / duration) * 100))
                progress_callback(pct)
    process.wait()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, cmd)
    if progress_callback:
        progress_callback(100)

def burn_captions(input_path, srt_path, output_path,
                  style=None, progress_callback=None):
    if style is None:
        style = get_caption_style('lesson')

    # size is stored as % of video height
    # libass FontSize uses a 288 DPI reference scale
    size_pct = style.get('size', 5)
    ffmpeg_font_size = max(6, round((size_pct / 100) * 288))
    
    # margin_bottom is in canvas pixels — convert to libass points
    # using same 288 DPI scale relative to a 1080p reference height
    margin_px = style.get('margin_bottom', 20)
    margin_v = max(0, round((margin_px / 1080) * 288))

    position = style.get('position', 'bottom')
    alignment = 6 if position == 'top' else 5 if position == 'middle' else 2

    style_str = (
        f"FontName={style['font']}"
        f",FontSize={ffmpeg_font_size}"
        f",PrimaryColour={style['colour']}"
        f",OutlineColour={style['outline_colour']}"
        f",Outline={style['outline']}"
        f",Shadow={style['shadow']}"
        f",Alignment={alignment}"
        f",MarginV={margin_v}"
    )
    safe_srt = srt_path.replace(':', '\\:')
    subtitle_filter = f"subtitles={safe_srt}:force_style='{style_str}'"

    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', subtitle_filter,
        '-c:a', 'copy',
        output_path
    ]

    if progress_callback:
        duration = get_video_duration(input_path)
        _run_ffmpeg_with_progress(cmd, duration, progress_callback)
    else:
        subprocess.run(cmd, check=True)

    print(f"Captions burned: {output_path}")

def export_final(input_path, output_path, target='landscape',
                 progress_callback=None):
    scale = '1920:1080' if target == 'landscape' else '1080:1920'
    cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', f'scale={scale}',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        output_path
    ]

    if progress_callback:
        duration = get_video_duration(input_path)
        _run_ffmpeg_with_progress(cmd, duration, progress_callback)
    else:
        subprocess.run(cmd, check=True)

    print(f"Exported: {output_path}")