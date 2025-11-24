import json
import os

STORAGE_FILE = 'user_channels.json'

def load_data():
    if not os.path.exists(STORAGE_FILE):
        return {}
    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_channel_count(user_id):
    data = load_data()
    return data.get(str(user_id), 0)

def increment_user_channel_count(user_id):
    data = load_data()
    user_id_str = str(user_id)
    current_count = data.get(user_id_str, 0)
    data[user_id_str] = current_count + 1
    save_data(data)
    return data[user_id_str]
