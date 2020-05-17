from talebearer_infra.support_libraries import logger
from functools import wraps
import json
import ast

def debug_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('Entering {0} with args {1} and kwargs {2}'.format(func.__name__, args, kwargs))
        try:
            return_value = func(*args, **kwargs)
        except:
            logger.debug('Exiting {0} with error..'.format(func.__name__))
            raise
        logger.debug('Exiting {0} with return value {1}'.format(func.__name__, return_value))
        return return_value
    return wrapper

class DebugMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if callable(value):
                local[attr] = debug_decorator(value)
        return type.__new__(cls, name, bases, local)
