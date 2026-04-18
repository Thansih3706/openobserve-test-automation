import time
from typing import Callable, Optional


def wait_until(
    condition: Callable[[], bool],
    timeout_seconds: int,
    interval_seconds: float = 1.0,
) -> bool:
    end_time = time.time() + timeout_seconds
    while time.time() < end_time:
        if condition():
            return True
        time.sleep(interval_seconds)
    return False


def get_nested(data: dict, *keys, default=None):
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current