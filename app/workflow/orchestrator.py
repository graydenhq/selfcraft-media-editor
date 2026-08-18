import os
import shutil
from app.ai.transcribe import transcribe, write_srt
from app.ai.silence import remove_silence
from app.ai.speaker import detect_speaker_name
from app.media.render import burn_captions, export_final
from app.export.naming import get_output_path
from app.logging.logger import get_logger
from app.core.config import get_folders, get_review_folder, subtitle_review_enabled
from database.db import update_progress, set_srt_path

log = get_logger("orchestrator")

def get_template(video_path):
    if "Teaching Reels" in video_path:
        return "reel"
    elif "Testimonials" in video_path:
        return "testimonial"
    else:
        return "lesson"

def process_phase1(video_path, video_id=None):
    """
    Phase 1: Transcribe and optionally pause for subtitle review.
    Returns 'awaiting_review' if review is enabled, or calls phase2 directly.
    """
    folders = get_folders()
    TEMP_FOLDER = folders['temp']
    REVIEW_FOLDER = get_review_folder()

    os.makedirs(TEMP_FOLDER, exist_ok=True)
    os.makedirs(REVIEW_FOLDER, exist_ok=True)
    log.info(f"Phase 1 starting: {video_path}")

    def report(msg):
        print(msg)
        if video_id:
            update_progress(video_id, msg)

    base_name = os.path.splitext(os.path.basename(video_path))[0]

    # Step 1: Transcribe
    report("Transcribing audio with Whisper AI…")
    result = transcribe(video_path)

    # Save SRT to review folder so it persists
    srt_path = os.path.join(REVIEW_FOLDER, f"{base_name}.srt")
    write_srt(result, srt_path)

    if video_id:
        set_srt_path(video_id, srt_path)

    if subtitle_review_enabled():
        report("Transcript ready — awaiting subtitle review…")
        log.info(f"Awaiting review: {srt_path}")
        return 'awaiting_review'
    else:
        return process_phase2(video_path, srt_path, video_id)


def process_phase2(video_path, srt_path, video_id=None, caption_style=None):
    folders = get_folders()
    EDITED_FOLDER = folders['edited_videos']
    TEMP_FOLDER = folders['temp']

    os.makedirs(EDITED_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    def report(msg):
        print(msg)
        if video_id:
            update_progress(video_id, msg)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    template = get_template(video_path)

    if template == "testimonial":
        report("Detecting speaker name from transcript…")
        from app.ai.speaker import detect_speaker_name
        with open(srt_path, 'r') as f:
            text = f.read()
        speaker_name, confidence = detect_speaker_name(text)
        if speaker_name:
            report(f"Speaker identified: {speaker_name}")
        else:
            report("Speaker not detected — continuing without name overlay")

    report("Removing silence from video…")
    silence_removed_path = os.path.join(TEMP_FOLDER, f"{base_name}_nosilence.mp4")
    actual_input = remove_silence(video_path, silence_removed_path, TEMP_FOLDER)

    report("Resizing video to target resolution…")
    target = 'landscape' if template == 'lesson' else 'reel'
    resized_path = os.path.join(TEMP_FOLDER, f"{base_name}_resized.mp4")
    export_final(actual_input, resized_path, target=target)

    report("Burning captions onto video…")
    # Use custom style from editor if provided, otherwise use config default
    if caption_style is None:
        caption_style = get_caption_style(template)
    captioned_path = os.path.join(TEMP_FOLDER, f"{base_name}_captioned.mp4")
    burn_captions(resized_path, srt_path, captioned_path, style=caption_style)

    report("Saving to Edited Videos…")
    output_path = get_output_path(video_path, EDITED_FOLDER)
    shutil.move(captioned_path, output_path)

    report("Cleaning up temporary files…")
    if os.path.exists(silence_removed_path):
        os.remove(silence_removed_path)
    os.remove(resized_path)
    if os.path.exists(srt_path):
        os.remove(srt_path)

    log.info(f"Completed: {output_path}")
    return output_path


# Keep backward compatibility
def process_video(video_path, video_id=None):
    return process_phase1(video_path, video_id)