#!/usr/bin/env python3
"""
exercise.py
"""
import redis
from uuid import uuid4 as uuid
from typing import Union


class Cache:
    def __init__(self) -> None:
        """
        Initialization.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that stores the input data in Redis
        using random key and return the key.
        """
        key = str(uuid())
        self._redis.set(key, data)
        return key
