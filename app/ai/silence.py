import subprocess
import re
import os

def detect_silence(video_path, noise_db=-30, min_duration=0.5):
    cmd = [
        'ffmpeg', '-i', video_path,
        '-af', f'silencedetect=noise={noise_db}dB:d={min_duration}',
        '-f', 'null', '-'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    log = result.stderr
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    return list(zip(starts, ends))

def get_video_duration(video_path):
    result = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ], capture_output=True, text=True)
    return float(result.stdout.strip())

def get_keep_segments(silences, video_duration, min_segment=0.5):
    keep = []
    cursor = 0.0
    for start, end in silences:
        if start - cursor >= min_segment:
            keep.append((cursor, start))
        cursor = end
    if video_duration - cursor >= min_segment:
        keep.append((cursor, video_duration))
    return keep

def remove_silence(video_path, output_path, temp_folder,
                   noise_db=-30, min_duration=0.5):
    silences = detect_silence(video_path, noise_db, min_duration)
    if not silences:
        print("No silences detected — skipping.")
        return video_path

    duration = get_video_duration(video_path)
    segments = get_keep_segments(silences, duration)
    if not segments:
        print("No keepable segments — skipping.")
        return video_path

    print(f"Removing {len(silences)} silence(s), keeping {len(segments)} segment(s)...")

    segment_files = []
    concat_list_path = os.path.join(temp_folder, "concat_list.txt")

    for i, (start, end) in enumerate(segments):
        seg_path = os.path.join(temp_folder, f"segment_{i:03d}.mp4")
        subprocess.run([
            'ffmpeg', '-y', '-i', video_path,
            '-ss', str(start), '-to', str(end),
            '-c', 'copy', seg_path
        ], capture_output=True, check=True)
        segment_files.append(seg_path)

    with open(concat_list_path, 'w') as f:
        for seg in segment_files:
            f.write(f"file '{seg}'\n")

    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', concat_list_path, '-c', 'copy', output_path
    ], check=True)

    for seg in segment_files:
        os.remove(seg)
    os.remove(concat_list_path)

    print(f"Silence removed: {output_path}")
    return output_path