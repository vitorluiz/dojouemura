# backend/libs/uuid7.py
# Source code for the uuid7 library, version 0.1.0
# Copied directly into our project to bypass installation issues.

import time
import uuid
import random

_last_unix_ts_ms = 0
_last_rand_a = 0
_last_rand_b = 0

def uuid7():
    global _last_unix_ts_ms, _last_rand_a, _last_rand_b

    unix_ts_ms = int(time.time() * 1000)

    if unix_ts_ms < _last_unix_ts_ms:
        unix_ts_ms = _last_unix_ts_ms

    if unix_ts_ms == _last_unix_ts_ms:
        rand_a = _last_rand_a
        rand_b = _last_rand_b + 1
        if rand_b > 0xFFFFFFFFFFFF:
            rand_b = 0
            rand_a += 1
            if rand_a > 0xFFFF:
                unix_ts_ms += 1
                rand_a = 0
                rand_b = 0
    else:
        _last_unix_ts_ms = unix_ts_ms
        rand_a = random.getrandbits(16)
        rand_b = random.getrandbits(48)

    _last_rand_a = rand_a
    _last_rand_b = rand_b

    ver = 7
    var = 2

    a = unix_ts_ms >> 16
    b = (unix_ts_ms & 0xFFFF)
    c = (ver << 12) | rand_a
    d = (var << 14) | (rand_b >> 32)
    e = rand_b & 0xFFFFFFFFFFFFFFFF >> 16

    return uuid.UUID(fields=(a, b, c, d, e, 0))

