#!/usr/bin/env python3
"""
exercise.py
"""
import redis
from uuid import uuid4 as uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(fn: Callable) -> Callable:
    """
    Function that counts how many times methods of
    the Cache class are called.
    """
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        self._redis.incr(fn.__qualname__)
        return fn(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self) -> None:
        """
        Initialization.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Method that stores the input data in Redis
        using random key and return the key.
        """
        key = str(uuid())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Method that takes a key and an optional fn.
        This fn will be used to convert the data back to the desired format.
        """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Automatically parametrize Cache.get
        with the correct conversion function.
        """
        return self.get(key, lambda data: data.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Automatically parametrize Cache.get
        with the correct conversion function.
        """
        return self.get(key, lambda data: int(data))
