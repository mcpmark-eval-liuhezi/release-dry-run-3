"""Small retry helper with exponential backoff.

Used by the telemetry client to harden its retry logic.
"""

import time

# Hard cap on retry attempts before giving up.
max_attempts = 5
base_delay = 0.5  # seconds
backoff_factor = 2.0


def retry(func, *args, **kwargs):
    """Call func(*args, **kwargs), retrying with exponential backoff.

    Waits base_delay * backoff_factor**(attempt - 1) seconds between
    attempts and gives up (re-raising the last exception) once the
    attempt cap is reached.
    """
    delay = base_delay
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as error:  # noqa: BLE001 - intentionally broad
            last_error = error
            if attempt >= max_attempts:
                break
            time.sleep(delay)
            delay *= backoff_factor

    raise last_error
