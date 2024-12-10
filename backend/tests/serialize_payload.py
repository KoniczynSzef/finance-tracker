from datetime import datetime
from decimal import Decimal
from typing import Any


def serialize_payload(payload: dict[str, Any]):
    for key, value in payload.items():
        if isinstance(value, Decimal):
            payload[key] = float(value)

        if isinstance(value, datetime):
            payload[key] = value.isoformat()

    return payload
