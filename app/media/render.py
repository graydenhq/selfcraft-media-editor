import subprocess
import os
import re
import threading
import tempfile
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
def _bgr_to_rgb(bgr_hex):
    """Convert FFmpeg BGR hex (&H00RRGGBB) to HTML RGB (#rrggbb)."""
    bgr_hex = bgr_hex.replace('&H', '').replace('&h', '')
    if len(bgr_hex) == 8:
        bgr_hex = bgr_hex[2:]  # strip alpha
    if len(bgr_hex) == 6:
        b = bgr_hex[0:2]
        g = bgr_hex[2:4]
        r = bgr_hex[4:6]
        return f'#{r}{g}{b}'
    return '#ffffff'

def _rgb_to_bgr(rgb_hex):
    """Convert HTML RGB (#rrggbb) to FFmpeg BGR hex (&H00BBGGRR)."""
    rgb_hex = rgb_hex.lstrip('#')
    if len(rgb_hex) == 6:
        r = rgb_hex[0:2]
        g = rgb_hex[2:4]
        b = rgb_hex[4:6]
        return f'&H00{b}{g}{r}'
    return '&H00FFFFFF'


def get_video_resolution(video_path):
    """Return (width, height) for the given video using ffprobe."""
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0:s=x', video_path
    ], capture_output=True, text=True)
    out = result.stdout.strip()
    if 'x' in out:
        try:
            w, h = out.split('x')
            return int(w), int(h)
        except Exception:
            return None, None
    return None, None


def _srt_time_to_ass(t):
    """Convert SRT time 'HH:MM:SS,mmm' to ASS time 'H:MM:SS.cc' (centiseconds)."""
    # Support both comma and dot
    t = t.replace('.', ',')
    parts = t.split(',')
    ms = int(parts[1]) if len(parts) > 1 else 0
    h, m, s = parts[0].split(':')
    cs = int(round(ms / 10.0))
    return f"{int(h)}:{int(m):02d}:{int(float(s)):02d}.{cs:02d}"


def srt_to_ass(srt_path, ass_path, style, playres):
    """Write a basic ASS file converted from SRT including a single Style.

    style: dict with keys like font, size, bold, italic, outline, shadow,
           colour (HTML or BGR), outline_colour (HTML or BGR), position, margin_bottom
    playres: (width, height)
    """
    width, height = playres
    size_pct = style.get('size', 5)
    # Font size in pixels based on video height
    font_px = max(6, round((size_pct / 100) * (height or 1080)))

    primary = style.get('colour', '&H00FFFFFF')
    outline = style.get('outline_colour', '&H00000000')
    if primary.startswith('#'):
        primary = _rgb_to_bgr(primary)
    if outline.startswith('#'):
        outline = _rgb_to_bgr(outline)

    bold = -1 if style.get('bold', False) else 0
    italic = -1 if style.get('italic', False) else 0
    outline_w = style.get('outline', 2)
    shadow = style.get('shadow', 1)
    position = style.get('position', 'bottom')
    margin_v = style.get('margin_bottom', 20)
    # ASS margins are pixels; we'll map margin_v relative to video height similar to before
    margin_ass_v = max(0, round((margin_v / (1080)) * (height or 1080)))

    # Alignment mapping already used: top=8, middle=5, bottom=2
    alignment = 2
    if position == 'top':
        alignment = 8
    elif position == 'middle':
        alignment = 5

    with open(srt_path, 'r', encoding='utf-8') as f:
        srt = f.read().strip()

    blocks = [b.strip() for b in srt.split('\n\n') if b.strip()]

    with open(ass_path, 'w', encoding='utf-8') as out:
        out.write('[Script Info]\n')
        out.write('ScriptType: v4.00+\n')
        out.write(f'PlayResX: {width or 1920}\n')
        out.write(f'PlayResY: {height or 1080}\n')
        out.write('\n')
        out.write('[V4+ Styles]\n')
        out.write('Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n')
        # Use sensible defaults for fields we don't expose
        out.write('Style: Default,')
        out.write(f"{style.get('font','Liberation Sans')},{font_px},{primary},&H00FFFFFF,{outline},&H00000000,{bold},{italic},0,0,100,100,0,0,1,{outline_w},{shadow},{alignment},10,10,{margin_ass_v},1\n")
        out.write('\n')
        out.write('[Events]\n')
        out.write('Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n')

        for blk in blocks:
            lines = blk.split('\n')
            if len(lines) < 3:
                continue
            # times line is second
            time_line = lines[1].strip()
            try:
                start_s, end_s = [t.strip() for t in time_line.split('-->')]
            except Exception:
                continue
            text = '\\N'.join([l.replace('\r','') for l in lines[2:]])
            start_ass = _srt_time_to_ass(start_s)
            end_ass = _srt_time_to_ass(end_s)
            # Escape commas are fine since Text is last field
            out.write(f'Dialogue: 0,{start_ass},{end_ass},Default,,0,0,0,,{text}\n')

def burn_captions(input_path, srt_path, output_path,
                  style=None, progress_callback=None):
    if style is None:
        style = get_caption_style('lesson')

    size_pct = style.get('size', 5)
    ffmpeg_font_size = max(6, round((size_pct / 100) * 288))

    margin_px = style.get('margin_bottom', 20)
    margin_v = max(0, round((margin_px / 1080) * 288))

    position = style.get('position', 'bottom')
    if position == 'top':
        alignment = 8
        margin_v = max(0, round((margin_px / 1080) * 288))
    elif position == 'middle':
        alignment = 5
        margin_v = 0
    else:  # bottom
        alignment = 2
        margin_v = max(0, round((margin_px / 1080) * 288))

    bold = 1 if style.get('bold', False) else 0
    italic = 1 if style.get('italic', False) else 0

    # Colour may come in as HTML (#rrggbb) from editor or BGR from config
    colour = style.get('colour', '&H00FFFFFF')
    outline_colour = style.get('outline_colour', '&H00000000')
    if colour.startswith('#'):
        colour = _rgb_to_bgr(colour)
    if outline_colour.startswith('#'):
        outline_colour = _rgb_to_bgr(outline_colour)

    # Create a temporary ASS file with styles and PlayRes matching the video
    width, height = get_video_resolution(input_path)
    if not width or not height:
        width, height = 1920, 1080

    # Ensure colours are in BGR form for ASS
    style_for_ass = dict(style)
    if style_for_ass.get('colour', '').startswith('#'):
        style_for_ass['colour'] = _rgb_to_bgr(style_for_ass['colour'])
    if style_for_ass.get('outline_colour', '').startswith('#'):
        style_for_ass['outline_colour'] = _rgb_to_bgr(style_for_ass['outline_colour'])

    ass_tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.ass')
    ass_path = ass_tmp.name
    ass_tmp.close()
    try:
        srt_to_ass(srt_path, ass_path, style_for_ass, (width, height))
        safe_ass = ass_path.replace(':', '\\:')
        subtitle_filter = f"subtitles={safe_ass}"

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
    finally:
        try:
            if os.path.exists(ass_path):
                os.remove(ass_path)
        except Exception:
            pass

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