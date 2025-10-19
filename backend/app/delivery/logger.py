import json, os
from datetime import datetime


def log_generation(user_id, signs, image_path):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "signs": signs,
        "image": image_path,
    }

    os.makedirs("app/logs", exist_ok=True)
    log_file = "app/logs/generation_log.jsonl"

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
