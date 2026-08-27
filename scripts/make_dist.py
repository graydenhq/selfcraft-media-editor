#!/usr/bin/env python3
"""Create a distributable zip where the launcher and README are at the archive root
and all other files/folders are placed under a single payload folder `sme_files/`.

Usage: python scripts/make_dist.py
Produces: dist/SelfCraft-Media-Editor.zip
"""
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'dist'
OUT_DIR.mkdir(exist_ok=True)
OUT_ZIP = OUT_DIR / 'SelfCraft-Media-Editor.zip'

EXCLUDE = {'.git', '.venv', 'dist', 'SelfCraft-Media-Editor.zip'}
LAUNCHER = 'SelfCraft Media Editor.bat'
README = 'README.md'
PAYLOAD_PREFIX = 'sme_files'

def add_file(z: zipfile.ZipFile, path: Path, arcname: str):
    z.write(path, arcname)

def main():
    if OUT_ZIP.exists():
        OUT_ZIP.unlink()

    with zipfile.ZipFile(OUT_ZIP, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        # Add launcher and README at root if present
        launcher_path = ROOT / LAUNCHER
        if launcher_path.exists():
            add_file(z, launcher_path, LAUNCHER)
        readme_path = ROOT / README
        if readme_path.exists():
            add_file(z, readme_path, README)

        # Add everything else under payload folder
        for item in sorted(ROOT.iterdir()):
            name = item.name
            if name in EXCLUDE or name in {LAUNCHER, README}:
                continue
            if item.is_dir():
                for root, dirs, files in os.walk(item):
                    for f in files:
                        full = Path(root) / f
                        rel = full.relative_to(ROOT)
                        arc = Path(PAYLOAD_PREFIX) / rel
                        add_file(z, full, str(arc))
            else:
                # top-level file
                arc = Path(PAYLOAD_PREFIX) / name
                add_file(z, item, str(arc))

    print('Created', OUT_ZIP)

if __name__ == '__main__':
    main()
