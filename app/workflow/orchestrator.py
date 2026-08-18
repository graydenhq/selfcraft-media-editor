import os
import shutil
from app.ai.transcribe import transcribe, write_srt
from app.ai.silence import remove_silence
from app.ai.speaker import detect_speaker_name
from app.media.render import burn_captions, export_final
from app.export.naming import get_output_path
from app.logging.logger import get_logger
from app.core.config import get_folders
from database.db import update_progress

log = get_logger("orchestrator")

def get_template(video_path):
    if "Teaching Reels" in video_path:
        return "reel"
    elif "Testimonials" in video_path:
        return "testimonial"
    else:
        return "lesson"

def process_video(video_path, video_id=None):
    folders = get_folders()
    EDITED_FOLDER = folders['edited_videos']
    TEMP_FOLDER = folders['temp']

    os.makedirs(EDITED_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    log.info(f"Starting: {video_path}")

    def report(msg):
        print(msg)
        if video_id:
            update_progress(video_id, msg)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    template = get_template(video_path)

    # Step 1: Transcribe
    report("Transcribing audio with Whisper AI…")
    result = transcribe(video_path)
    srt_path = os.path.join(TEMP_FOLDER, f"{base_name}.srt")
    write_srt(result, srt_path)

    # Step 2: Speaker detection for testimonials
    if template == "testimonial":
        report("Detecting speaker name from transcript…")
        speaker_name, confidence = detect_speaker_name(result['text'])
        if speaker_name:
            report(f"Speaker identified: {speaker_name}")
        else:
            report("Speaker not detected — continuing without name overlay")

    # Step 3: Remove silence
    report("Removing silence from video…")
    silence_removed_path = os.path.join(TEMP_FOLDER, f"{base_name}_nosilence.mp4")
    actual_input = remove_silence(video_path, silence_removed_path, TEMP_FOLDER)

    # Step 4: Resize
    report("Resizing video to target resolution…")
    target = 'landscape' if template == 'lesson' else 'reel'
    resized_path = os.path.join(TEMP_FOLDER, f"{base_name}_resized.mp4")
    export_final(actual_input, resized_path, target=target)

    # Step 5: Burn captions onto correctly sized video
    report("Burning captions onto video…")
    captioned_path = os.path.join(TEMP_FOLDER, f"{base_name}_captioned.mp4")
    burn_captions(resized_path, srt_path, captioned_path)

    # Step 6: Move to Edited Videos with versioned name
    report("Saving to Edited Videos…")
    output_path = get_output_path(video_path, EDITED_FOLDER)
    shutil.move(captioned_path, output_path)

    # Step 7: Clean up
    report("Cleaning up temporary files…")
    if os.path.exists(silence_removed_path):
        os.remove(silence_removed_path)
    os.remove(resized_path)
    os.remove(srt_path)

    log.info(f"Completed: {output_path}")
    return output_path