SME Specification Audit and Implementation Plan
=============================================

Generated: 2026-08-27

Summary
-------
This document records the audit I performed comparing `SME_Specification_v1.0.md`
to the repository implementation, the gaps found, prioritized recommendations,
estimated effort, and a concrete step-by-step plan for closing high-priority
gaps. It also documents the branch/commit plan for delivering changes.

Audit findings (mapping)
------------------------
- Folder watcher & detection
  - Implemented: `app/core/main.py` watcher (`VideoHandler`) and `database/db.py:add_video()`.

- Transcription (Whisper)
  - Implemented: `app/ai/transcribe.py` with lazy-loading model; `scripts/setup.bat`
    now prompts for a model and downloads using `whisper.load_model()`.

- Silence removal, speaker detection, pipeline orchestration
  - Implemented: `app/workflow/orchestrator.py` calls `transcribe`, `remove_silence`, and `detect_speaker_name`.

- SRT→ASS conversion and correct burning
  - Implemented: `app/media/render.py` has `srt_to_ass()` with PlayRes set to video resolution and `burn_captions()` using ffmpeg subtitles filter.

- Export and versioned naming
  - Implemented: `app/media/render.py:export_final()` and `app/export/naming.py` are used by the orchestrator.

- DB with duration caching and backfill
  - Implemented: `database/db.py` includes `duration` column, `backfill_durations()`.

- Frontend dashboard & subtitle editor
  - Present in repo root and served at `/` by `app/core/main.py`.

- Packaging / ZIP distribution & launcher
  - Implemented: scripts to create `dist/SelfCraft-Media-Editor.zip`; top-level launcher exists.

Gaps (spec → implementation)
-----------------------------
The following items are required by `SME_Specification_v1.0.md` (v1.0 scope) but are missing or only partially implemented:

1) Thumbnail & preview generation (FR-002 / FR-003) — MISSING / HIGH PRIORITY
   - Spec requires generating preview thumbnails for every video and previews available before editing. The repo currently does not generate or persist thumbnails or preview clips on detection.

2) Automated Quality Review Engine (FR-011) — MISSING / HIGH PRIORITY
   - Spec expects an AI-driven quality review with pass/warning/failed statuses (checks: audio quality, captions present, branding, export quality). There is no such module.

3) Asset Management (MAM) — MISSING / MEDIUM PRIORITY
   - The spec requires centrally managed intros/outros/fonts/logos and editable assets. No asset DB, upload UI, or asset application logic exists.

4) Advanced Template Behaviors — PARTIAL / MEDIUM
   - Basic template selection is implemented (folder-based). Advanced behaviors (dynamic cuts, zoom/motion effects, CTAs, intro/outro insertion) are not implemented.

5) Tests / CI / Schema-migrations — PARTIAL / MEDIUM
   - No automated tests or migration tooling beyond pragmatic ALTER TABLEs. Adding tests and lightweight migration tooling recommended.

6) Packaging UX notes — ADDITIONAL IMPROVEMENTS / LOW
   - The Windows `setup.bat` now prompts for model but should warn for large models and validate disk/RAM before downloading. Add `dist/README_INSTALL.txt` and the zip SHA256.

Prioritized recommendations (what to do first)
-------------------------------------------
I recommend the following ordered work plan (short, actionable items that align with v1.0 binding scope):

1) Implement thumbnail and preview generation (HIGH)
   - Add `app/media/preview.py` to create: `thumbnail` (single image) and `preview` (short 3–6s mp4/webm). Store paths in DB columns `thumbnail_path`, `preview_path` (add migration).
   - Call generation at detection time (watcher -> add_video) so thumbnails are available immediately. Provide DB defaults and backfill tool for existing rows.
   - Example ffmpeg commands:

     - Thumbnail (single frame at 3s):
       ```bash
       ffmpeg -ss 00:00:03 -i input.mp4 -frames:v 1 -q:v 2 -vf scale=320:-1 thumb.jpg
       ```

     - Preview clip (3s, scaled):
       ```bash
       ffmpeg -ss 00:00:02 -i input.mp4 -t 3 -c:v libx264 -crf 28 -vf scale=480:-2 -c:a aac -b:a 64k preview.mp4
       ```

   - Estimate: small → medium effort (1–2 days). High-impact: fulfils FR-002/FR-003.

2) Implement minimal Quality Review engine (HIGH)
   - Create `app/quality/reviewer.py` with checks (examples):
     - Video resolution/frame-rate matches template expectations (ffprobe)
     - Captions present and non-empty (SRT file existence and length)
     - Audio loudness/peak within reasonable ranges (use `ffmpeg` loudnorm or `pydub`/`librosa` computations)
     - Speaker detection pass for testimonials (reuse `detect_speaker_name`) and transcription confidence threshold
   - At end of `process_phase2`, run review and store `quality_status` and `quality_score` in DB; show status in dashboard `/videos`.
   - Estimate: medium (2–4 days).

3) Add Asset Management basics (MEDIUM)
   - Create `assets/` folder and DB table `assets(id, type, path, meta...)` and minimal UI to upload/select per-template assets.
   - Integrate with `process_phase2` for simple intro/outro concatenation and watermark overlays.
   - Estimate: medium → large depending on UI (3–7 days).

4) Improve Windows setup model-download UX (SMALL)
   - Add `scripts/download_model.py` which runs `whisper.load_model()` and prints progress or at least displays disk space/size warning for medium/large models.
   - Update `setup.bat` to call it and prompt for confirmation for large downloads.
   - Estimate: small (0.5 day).

5) Add automated tests, lightweight migration helper and CI (MEDIUM)
   - Add a `tests/` folder with unit tests for `srt_to_ass`, `get_video_resolution`, DB operations, and a smoke test for `process_phase1` with a short test fixture video.
   - Add a simple migration utility script to add new columns safely and record schema version (or adopt Alembic if you prefer a full solution).
   - Estimate: medium (2–4 days).

6) Packaging improvements (LOW)
   - Inject `dist/README_INSTALL.txt` into the zip with SHA256 and model size table; optionally include a `verify_install.ps1` for Windows.
   - Estimate: small (1–2 hours).

Concrete implementation plan for the thumbnail feature (detailed)
-------------------------------------------------------------
Files to add/modify:
- `app/media/preview.py` (new)
- `database/db.py` (add `thumbnail_path`, `preview_path` columns and backfill function)
- `app/core/main.py` or `app/workflow/watcher` (call preview generation on new file)
- Frontend `dashboard.html` (use thumbnail path from `/videos` and show preview on hover/click)

Preview module pseudocode:

```
def generate_thumbnail(input_path, output_dir):
    # ensure output_dir exists
    # compute duration
    # pick timestamp = min(3, duration/4)
    # run ffmpeg to generate scaled jpeg
    return thumb_path

def generate_preview(input_path, output_dir, duration=3):
    # cut 3s clip starting at 2s (or earlier if too short), scale down
    return preview_path

def generate_and_store(input_path, db_row_id, output_dir):
    thumb = generate_thumbnail(...)
    preview = generate_preview(...)
    update_db(db_row_id, thumbnail_path=thumb, preview_path=preview)
```

DB migration notes
------------------
- `database/db.py` should be updated to add `thumbnail_path TEXT, preview_path TEXT` during `init_db()` if missing, similar to existing pragmatic ALTER TABLE logic.
- Add `backfill_previews()` that computes thumbnails/previews for rows missing them.

Branching, commit, and push plan
--------------------------------
- Branch: `spec-audit` (feature branch for spec audit and follow-up changes)
- Commit message for this file: "docs: add spec audit, gap analysis, and implementation plan"
- After implementing thumbnails and quality review, open PR targeting `main` with incremental commits and clear PR description linking to this plan file.

Next steps I will take if you confirm
-------------------------------------
1) Implement the thumbnail/preview pipeline (create code, tests, DB migration, small dashboard changes) on branch `spec-audit/preview` and open a PR.
2) Implement the quality review engine as a follow-up branch `spec-audit/quality`.

Contact and notes
-----------------
If you want me to start implementing step 1 now, I will create the new module, update DB, add unit tests, and run the local checks. Otherwise tell me which step to start first.

End of document
