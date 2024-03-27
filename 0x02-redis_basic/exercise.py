#!/usr/bin/env python3
"""
exercise.py
"""
import redis
from uuid import uuid4 as uuid
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A count_calls decorator to store
    call count for a particular method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A call_history decorator to store the history of
    inputs and outputs for a particular method.
    """
    @wraps((method))
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function.
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", output)
        return output
    return wrapper


class Cache:
    def __init__(self) -> None:
        """
        Initialization.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
