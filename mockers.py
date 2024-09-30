import random
import string
from datetime import datetime, timedelta


def or_null(generator_func):
    def nullable_generator(*args, nullable=False):
        if nullable and random.random() < 0.5:
            return None
        return generator_func(*args)

    return nullable_generator


def generate_number():
    return str(random.randint(0, 100))


@or_null
def generate_id():
    return str(random.randint(0, 2**63 - 1))


@or_null
def generate_string(length):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@or_null
def generate_random_date():
    return (datetime.utcnow() - timedelta(minutes=random.randint(0, 600))).isoformat()
