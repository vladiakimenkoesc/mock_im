import json
import random


def generate_id(existing_ids):
    while str(new_id := random.randint(0, 2**63 - 1)) in existing_ids:
        pass
    return str(new_id)


def save_messages_to_file(messages, file_path):
    with open(file_path, "w") as f:
        json.dump(messages, f, indent=4)


def load_messages_from_file(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def update_existing_ids(file_path, existing_ids):
    with open(file_path, "r") as f:
        messages = json.load(f)
    for msg in messages:
        existing_ids.add(msg["id"])
        if "updateId" in msg and msg["updateId"] is not None:
            existing_ids.add(msg["updateId"])
