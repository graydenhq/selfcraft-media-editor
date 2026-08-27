#!/usr/bin/env python3
"""Download a Whisper model with user confirmation and disk-space checks.

Usage: python scripts/download_model.py <model>
"""
import sys
import shutil
import os

MODEL_SIZES_MB = {
    'tiny': 75,
    'base': 140,
    'small': 460,
    'medium': 1500,
    'large': 5000,
}


def human_mb(mb):
    if mb >= 1024:
        return f"{mb/1024:.1f} GB"
    return f"{mb} MB"


def main():
    if len(sys.argv) < 2:
        print('Usage: download_model.py <model>')
        print('Models: ' + ', '.join(MODEL_SIZES_MB.keys()))
        return 2

    model = sys.argv[1]
    if model not in MODEL_SIZES_MB:
        print(f"Unknown model '{model}'. Known: {', '.join(MODEL_SIZES_MB.keys())}")
        return 2

    est_mb = MODEL_SIZES_MB[model]
    total, used, free = shutil.disk_usage(os.getcwd())
    free_mb = free // (1024 * 1024)

    print(f"Selected Whisper model: {model} (approx {human_mb(est_mb)})")
    print(f"Disk free: {human_mb(free_mb)}")

    if free_mb < est_mb + 200:
        print('WARNING: You appear to have less than recommended free disk space for this model.')
        print('It is recommended to free up at least an additional 200 MB before continuing.')

    if est_mb >= 1500:
        confirm = input('This model is large and may take a long time. Continue? [y/N]: ').strip().lower()
        if confirm not in ('y', 'yes'):
            print('Cancelled by user.')
            return 1
    else:
        confirm = input('Download model now? [Y/n]: ').strip().lower()
        if confirm not in ('', 'y', 'yes'):
            print('Cancelled by user.')
            return 1

    try:
        import whisper
        print('Downloading model via whisper.load_model() — this may take several minutes...')
        whisper.load_model(model)
        print('Model download complete.')
        return 0
    except Exception as e:
        print('Model download failed:', e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
