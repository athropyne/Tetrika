from functools import wraps
from typing import Callable
import inspect


def strict(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sign = inspect.signature(func).parameters
        types = [t.annotation for t in sign.values()]
        inputs = list(args) + [v for v in kwargs.values()]
        for i in range(len(types)):
            if not isinstance(inputs[i], types[i]):
                raise TypeError(f"переданное значение {inputs[i]} не соответствует типу {types[i]}")
        return func(*args, **kwargs)

    return wrapper
