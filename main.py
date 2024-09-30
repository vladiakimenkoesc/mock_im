import logging
import random
from enum import Enum
from uuid import uuid4

from flask import Flask, jsonify, request

from mockers import generate_id, generate_random_date, generate_string


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
app = Flask(__name__)

ITEMS_PER_RESPONSE = 10
known_user_ids = [generate_id() for _ in range(10)]


class EntityType(Enum):
    UNKNOWN = "messageEntityUnknown"
    PRE = "messageEntityPre"
    TEXT_URL = "messageEntityTextUrl"
    MENTION_NAME = "messageEntityMentionName"
    INPUT_MENTION_NAME = "inputMessageEntityMentionName"
    CUSTOM_EMOJI = "messageEntityCustomEmoji"


class Direction(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class MessageEntityType(Enum):
    EMPTY = "inputUserEmpty"


def generate_entity():
    entity_type = random.choice(list(EntityType))
    entity = {
        "type": entity_type.value,
        "offset": generate_string(5),
        "length": generate_string(3),
    }
    if entity_type == EntityType.PRE:
        entity["language"] = generate_string(2).lower()
    elif entity_type == EntityType.TEXT_URL:
        entity["url"] = f"https://example.com/{generate_string(10)}"
    elif entity_type == EntityType.MENTION_NAME:
        entity["userId"] = generate_id()
    elif entity_type == EntityType.INPUT_MENTION_NAME:
        entity["userId"] = {"type": MessageEntityType.EMPTY.value}
    elif entity_type == EntityType.CUSTOM_EMOJI:
        entity["documentId"] = generate_id()
    return entity


def generate_feed_item():
    return {
        "id": generate_id(),
        "updateId": generate_id(nullable=True),
        "userId": generate_id() if random.random() > 0.7 else random.choice(known_user_ids),
        "created": generate_random_date(),
        "direction": random.choice([d.value for d in Direction]),
        "clientId": str(uuid4()),
        "entities": [generate_entity() for _ in range(random.randint(1, 6))],
        "replyToMessageId": generate_id(nullable=True),
        "message": generate_string(100),
        "media": generate_string(16, nullable=True),
        "edited": generate_random_date(nullable=True),
        "grouppedId": generate_id(nullable=True),
    }


@app.route("/listDifferenceV1", methods=["PUT"])
def list_difference_v1():
    logger.info(f"Incoming {request.method} request {request.url}")
    logger.info(f"{request.get_json()}")
    feed = [generate_feed_item() for _ in range(ITEMS_PER_RESPONSE)]
    has_more = random.choice([True, False])
    return jsonify({"hasMore": has_more, "feed": feed})


@app.route("/typingV1", methods=["PUT"])
def typing_v1():
    logger.info(f"Incoming {request.method} request {request.url}")
    logger.info(f"{request.get_json()}")
    return jsonify({"type": "success"})


@app.route("/sendV1", methods=["PUT"])
def send_v1():
    logger.info(f"Incoming {request.method} request {request.url}")
    logger.info(f"{request.get_json()}")
    return jsonify({"type": "success", "messageId": generate_id()})


@app.route("/assistant", methods=["POST"])
def assistance():
    logger.info(f"Incoming {request.method} request {request.url}")
    logger.info(f"{request.get_json()}")
    return jsonify(
        {
            "response": generate_string(50),
            "metadata": {},
            "logs": {
                "intents": {
                    generate_string(10): [
                        generate_string(10) for _ in range(random.randint(1, 5))
                    ]
                    for __ in range(random.randint(0, 3))
                },
                "task_detected": random.choice([True, False]),
                "links": [
                    f"https://{generate_string(10)}.com/{generate_string(10)}"
                    for _ in range(random.randint(0, 3))
                ],
                "thread_id": "",
            },
        }
    )


if __name__ == "__main__":
    app.run(port=5050)
