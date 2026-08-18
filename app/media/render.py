import subprocess
from app.core.config import get_caption_style

def burn_captions(input_path, srt_path, output_path, style=None):
    if style is None:
        style = get_caption_style('lesson')

    position = style.get('position', 'bottom')
    if position == 'top':
        alignment = 6
        margin_v = style.get('margin_bottom', 20)
    elif position == 'middle':
        alignment = 5
        margin_v = 0
    else:  # bottom
        alignment = 2
        margin_v = style.get('margin_bottom', 20)

    style_str = (
        f"FontName={style['font']}"
        f",FontSize={style['size']}"
        f",PrimaryColour={style['colour']}"
        f",OutlineColour={style['outline_colour']}"
        f",Outline={style['outline']}"
        f",Shadow={style['shadow']}"
        f",Alignment={alignment}"
        f",MarginV={margin_v}"
    )
    safe_srt = srt_path.replace(':', '\\:')
    subtitle_filter = f"subtitles={safe_srt}:force_style='{style_str}'"
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vf', subtitle_filter,
        '-c:a', 'copy',
        output_path
    ], check=True)
    print(f"Captions burned: {output_path}")

def export_final(input_path, output_path, target='landscape'):
    scale = '1920:1080' if target == 'landscape' else '1080:1920'
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vf', f'scale={scale}',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
        '-c:a', 'aac', '-b:a', '192k',
        output_path
    ], check=True)
    print(f"Exported: {output_path}")