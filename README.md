# SelfCraft Media Editor (SME)

An automated video post-production tool for SelfCraft Academy. Drop a raw
video into the right folder — SME transcribes it, burns captions, and exports
a clean finished video. The original is never touched.

---

## What It Does

- Watches folders for new video files automatically
- Reads programme, week, module, and lesson info from the folder structure
- Transcribes audio using Whisper AI (runs fully offline after first run)
- Burns captions onto the video at the correct size
- Exports Recorded Lessons in landscape (1920×1080) and Reels/Testimonials
  in vertical (1080×1920)
- Saves output as `Lesson Name (Edited).mp4` — never overwrites originals
- Browser-based dashboard with live progress updates

---

## Requirements

- Python 3.11 or newer
- FFmpeg
- Git

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davidowoh/selfcraft-media-editor.git
cd selfcraft-media-editor
```

### 2. Create and activate a virtual environment

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
# Install CPU-only PyTorch first (avoids downloading 2GB+ of GPU libraries)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Then install the rest
pip install fastapi uvicorn openai-whisper watchdog python-multipart
```

### 4. Install FFmpeg

**Fedora Linux:**
```bash
sudo dnf install ffmpeg
```

**Ubuntu / Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
```
winget install ffmpeg
```

### 5. Install tkinter (for folder picker in Settings)

**Fedora Linux:**
```bash
sudo dnf install python3-tkinter
```

**Ubuntu / Debian:**
```bash
sudo apt install python3-tk
```

**Windows:** tkinter is included with Python — no separate install needed.

---

## Configuration

Open `config/settings.json` and update the folder paths to match your machine:

```json
{
  "folders": {
    "raw_videos": "/your/path/to/SelfCraft Media/Raw Videos",
    "edited_videos": "/your/path/to/SelfCraft Media/Edited Videos",
    "temp": "/your/path/to/SelfCraft Media/Temp"
  },
  "file_manager": "nautilus",
  "video_player": "browser",
  "captions": {
    "font": "Liberation Sans",
    "size": 14,
    "colour": "&H00FFFFFF",
    "outline_colour": "&H00000000",
    "outline": 2,
    "shadow": 1,
    "margin_bottom": 20
  },
  "whisper_model": "base",
  "max_parallel_jobs": 1
}
```

You can also change all settings from the Settings panel inside the dashboard
without editing this file manually.

---

## Folder Structure

Create this folder structure on your machine before running the app
(or configure different paths in Settings):

```
SelfCraft Media/
  Raw Videos/
    Recorded Classes/
      Programme Name/
        Week 1/
          Module 1/
            Lesson 1 - Title.mp4
    Teaching Reels/
    Testimonials/
  Edited Videos/
  Temp/
```

The folder names feed the metadata system directly — SME reads programme,
week, module, and lesson information from the path automatically.

---

## Running the App

### Start the server

**Linux / macOS:**
```bash
source .venv/bin/activate
uvicorn app.core.main:app --reload
```

**Windows:**
```
.venv\Scripts\activate
uvicorn app.core.main:app --reload
```

### Open the dashboard

Open `dashboard.html` directly in your browser.

**Linux:**
```bash
xdg-open dashboard.html
```

Or drag the file into a browser window.

The dashboard connects to the server at `http://127.0.0.1:8000`.

---

## First Run

The first time Whisper runs it downloads a model the first time it's used.
During `setup.bat` on Windows you will be prompted which Whisper model to
download. Choose based on the trade-off between speed, RAM usage, and
transcription accuracy:

- `tiny` — ~75 MB (fastest, lowest accuracy)
- `base` — ~140 MB (good balance, default)
- `small` — ~460 MB (better accuracy, slower)
- `medium` / `large` — progressively larger (1.5 GB+, 5GB+) — only choose
  these if you have the disk space and need the best possible accuracy.

An internet connection is required for the model download. Once downloaded
into the virtual environment, transcription runs fully offline. The
Windows `setup.bat` will show the prompt and then call Python to download
the selected model into `.venv` (this can take several minutes for larger
models).

---

## Using the Dashboard

| Button | What it does |
|---|---|
| ▶ Process | Run the full pipeline on this video |
| ↺ Re-run | Process again — creates a versioned copy (v2, v3…) |
| ↺ Retry | Re-attempt a failed job |
| ▶ Raw | Play the original unedited video |
| ▶ Edited | Play the latest edited output |
| 📂 Raw Videos | Open the Raw Videos folder in your file manager |
| 🎬 Edited Videos | Open the Edited Videos folder |
| 🗑 Clear Completed | Remove completed jobs from the list (files are kept) |
| ⚙️ Settings | Change folder paths, caption style, Whisper model |

---

## Supported Video Types

| Type | Folder | Output |
|---|---|---|
| Recorded Lesson | `Recorded Classes/` | 1920×1080 landscape |
| Teaching Reel | `Teaching Reels/` | 1080×1920 vertical |
| Testimonial | `Testimonials/` | 1080×1920 vertical |

---

## Troubleshooting

**Dashboard shows red "Cannot reach backend"**
The server is not running. Start it with `uvicorn app.core.main:app --reload`.

**Video stuck on "processing" after restart**
Normal — the app detects this on startup and resets stuck jobs to "detected"
automatically. Click Retry on any stuck job.

**Captions not appearing**
Check that the `.srt` file was generated in the Temp folder during processing.
Very quiet or muffled audio may produce no transcript.

**FFmpeg not found**
Run `ffmpeg -version` in your terminal. If it fails, reinstall FFmpeg and
make sure it is added to your PATH.

**Folder picker (Browse button) not working on Linux**
Install tkinter: `sudo dnf install python3-tkinter` (Fedora) or
`sudo apt install python3-tk` (Ubuntu).

---

## Tech Stack

| Component | Tool |
|---|---|
| Backend | Python, FastAPI |
| Transcription | OpenAI Whisper (local, offline) |
| Video processing | FFmpeg |
| Database | SQLite |
| Folder watching | watchdog |
| Frontend | Plain HTML/CSS/JS |

---

## Notes for Windows Users

### First-time setup

Windows users can run `setup.bat` (double-click it) for fully automatic
setup — it installs dependencies, creates the virtual environment, creates
media folders on the Desktop, and configures paths automatically.

After that, double-click `start.bat` every time you want to use the app.

### Manual setup (if setup.bat doesn't work)

1. Install Python from **python.org/downloads** — tick
   **"Add python.exe to PATH"** on the first installer screen
2. Install Git from **git-scm.com** — accept all defaults
3. Open a terminal as Administrator and run:
   `winget install ffmpeg` — then close and reopen the terminal
4. Clone this repo and navigate into it
5. Create the virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
6. Install libraries:
   ```
   # Install CPU-only PyTorch first (avoids downloading 2GB+ of GPU libraries)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Then install the rest
pip install fastapi uvicorn openai-whisper watchdog python-multipart
   ```
7. Open `config/settings.json` in Notepad and update folder paths.
   Use forward slashes and change `file_manager` to `explorer`:
   ```json
   "raw_videos": "C:/Users/YourName/Desktop/SelfCraft Media/Raw Videos",
   "file_manager": "explorer"
   ```

### Every time you use SME on Windows

```
cd path\to\selfcraft-media-editor
.venv\Scripts\activate
uvicorn app.core.main:app --reload
```

Then open `dashboard.html` in your browser.

### Windows-specific notes

- tkinter is bundled with Python on Windows — no separate install needed
- Use the Browse button in Settings to set folder paths without typing
- Change `file_manager` to `explorer` in settings
- Leave the terminal window open while using the app — closing it stops the server
- If FFmpeg is not found after install, restart your computer

---

*SelfCraft Academy — internal tooling*
*Built with Python, FastAPI, Whisper, and FFmpeg*
