Packaging and Distribution
=========================

This project can be packaged for distribution so users extract a single top-level
`SelfCraft Media Editor.bat` file alongside the required folders. The bundle
includes the repository contents (excluding `.git` and `.venv`).

Quick steps
-----------
- Windows: run `scripts\package.bat` to create `SelfCraft-Media-Editor.zip`.
- Linux/macOS: run `scripts/package.sh` to create `SelfCraft-Media-Editor.tar.gz`.

Run flow after extraction
-------------------------
1. Double-click `SelfCraft Media Editor.bat`.
   - If this is the first run, the script runs `scripts\setup.bat` to create
     a Python virtual environment, install dependencies, and configure folders.
   - On subsequent runs it runs `scripts\start.bat`, which starts the server
     and opens the UI at `http://127.0.0.1:8000/`.

Why we serve `http://127.0.0.1:8000/` instead of using `file://`:
- Serving the frontend gives the same origin as the API (`/videos`, etc.),
  avoiding file-origin restrictions and making fetch/XHR and media loading reliable.
- `127.0.0.1` is local-only; the server is not exposed to the network.

Notes
-----
- The Windows packaging excludes `.git` and `.venv` via `scripts\package.bat`.
- The POSIX `scripts/package.sh` creates a `.tar.gz` archive and excludes the
  same directories.
- If you later want multi-device access on your LAN, change the server host
  to `0.0.0.0` and open `http://<host-ip>:8000/`, but be careful about exposure.

Next steps (optional)
---------------------
- Add a small installer that creates desktop shortcuts and registers file types.
- Create a signed single-executable wrapper if you need a truly single-file
  distribution.
