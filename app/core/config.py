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