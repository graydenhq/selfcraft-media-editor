import json
import os

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'config', 'settings.json'
)

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_folders():
    return load_config()['folders']

def get_caption_style(video_type='lesson'):
    captions = load_config()['captions']
    # Support both old flat format and new per-type format
    if 'lesson' in captions:
        return captions.get(video_type, captions.get('lesson'))
    return captions  # backward compat

def get_file_manager():
    return load_config().get('file_manager', 'nautilus')

def get_whisper_model():
    return load_config().get('whisper_model', 'base')

def get_video_player():
    return load_config().get('video_player', 'browser')

def get_review_folder():
    return load_config().get(
        'review_folder',
        os.path.expanduser('~/SelfCraft Media/Review')
    )

def subtitle_review_enabled():
    return load_config().get('subtitle_review', True)

def bgr_to_rgb(bgr_hex):
    bgr_hex = bgr_hex.replace('&H', '').replace('&h', '')
    if len(bgr_hex) == 8:
        bgr_hex = bgr_hex[2:]
    if len(bgr_hex) == 6:
        b, g, r = bgr_hex[0:2], bgr_hex[2:4], bgr_hex[4:6]
        return f'#{r}{g}{b}'
    return '#ffffff'