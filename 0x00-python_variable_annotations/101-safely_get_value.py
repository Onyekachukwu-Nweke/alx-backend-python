#!/usr/bin/env python3
"""Given the parameters and the return values,
add type annotations to the function"""
from typing import Mapping, TypeVar, Any, Union


T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """return the value of a dict key if key is present in dict passed
    else returns None"""
    if key in dct:
        return dct[key]
    else:
        return default
