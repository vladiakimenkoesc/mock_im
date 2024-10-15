import logging
import os
from datetime import datetime
from enum import Enum
from uuid import uuid4

from flask import Flask, jsonify, make_response, request

from utils import generate_id, load_messages_from_file, save_messages_to_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
app = Flask(__name__)

RESPONSE_FILE = "replies/replies.txt"
ITEMS_PER_RESPONSE = int(os.environ["ITEMS_PER_RESPONSE"])
FILE_PATH = os.environ["FEED_FILE_PATH"]
messages_bank = load_messages_from_file(FILE_PATH)
existing_ids = {msg["id"] for msg in messages_bank}
assistant_id = generate_id(existing_ids)


class Direction(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


@app.route("/listDifferenceV1", methods=["PUT"])
def list_difference_v1():
    logger.debug(f"Incoming {request.method} request {request.url}")
    logger.debug(f"{request.get_json()}")
    global messages_bank
    messages_bank = load_messages_from_file(FILE_PATH)
    from_update_id = request.get_json().get("fromUpdateId")
    start_index = next(
        (index for index, msg in enumerate(messages_bank) if msg["updateId"] == from_update_id), -1
    )
    feed = messages_bank[start_index + 1: start_index + 1 + ITEMS_PER_RESPONSE]
    has_more = (start_index + 1 + ITEMS_PER_RESPONSE) < len(messages_bank)
    return jsonify({"hasMore": has_more, "feed": feed})


# @app.route("/typingV1", methods=["PUT"])
# def typing_v1():
#     logger.debug(f"Incoming {request.method} request {request.url}")
#     logger.debug(f"{request.get_json()}")
#     return jsonify({"type": "success"})


@app.route("/sendV1", methods=["PUT"])
def send_v1():
    logger.debug(f"Incoming {request.method} request {request.url}")
    payload = request.get_json()
    logger.debug(f"{payload}")

    message_content = payload.get("message")
    client_id = payload.get("clientId")

    with open(RESPONSE_FILE, "at") as f:
        f.write(f"Response to {client_id=}: {message_content}\n")

    new_id = generate_id(existing_ids)
    new_message = {
        "id": new_id,
        "updateId": new_id,
        "userId": assistant_id,
        "created": datetime.utcnow().isoformat(),
        "direction": Direction.OUTBOUND,
        "clientId": client_id,
        "entities": [],
        "replyToMessageId": None,
        "message": message_content,
        "media": None,
        "edited": None,
        "grouppedId": None,
    }
    existing_ids.add(new_id)
    messages_bank.append(new_message)
    save_messages_to_file(messages_bank, FILE_PATH)

    return jsonify({"type": "success", "messageId": new_message["id"]})


@app.route("/add", methods=["PUT"])
def add():
    payload = request.get_json()

    message_content = payload.get("message")
    if not message_content:
        return make_response(jsonify({"error": "message should be provided"}), 400)
    from_id = payload.get("fromId", generate_id(existing_ids))
    reply_to = payload.get("replyToMessageId", None)

    message_id = generate_id(existing_ids)
    new_message = {
        "id": message_id,
        "updateId": message_id,
        "userId": from_id,
        "created": datetime.utcnow().isoformat(),
        "direction": Direction.INBOUND,
        "clientId": str(uuid4()),
        "entities": [],
        "replyToMessageId": reply_to,
        "message": message_content,
        "media": None,
        "edited": None,
        "grouppedId": None,
    }
    existing_ids.add(message_id)
    messages_bank.append(new_message)
    save_messages_to_file(messages_bank, FILE_PATH)

    return make_response("success", 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)

