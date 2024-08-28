from time import sleep
from typing import Callable, Union
import concurrent.futures
from functools import wraps
from random import choice

from .logger import logger


def backoff(start_sleep_time: Union[int, float] = 0.1,
            factor: Union[int, float] = 2,
            border_sleep_time: Union[int, float] = 10,
            timeout: Union[int, float] = 5,
            exceptions: tuple = ()
            ) -> Callable:
    """
        A decorator that retries a function with an exponential backoff and timeouts.

        Formula:
            t = start_sleep_time * (factor ^ n) if t < border_sleep_time
            t = border_sleep_time, otherwise

        :param start_sleep_time: Initial waiting time
        :param factor: The factor by which the wait time increases each iteration
        :param border_sleep_time: The maximum wait time
        :param timeout: Time to wait for a function's response before retrying
        :param exceptions: A tuple of exception types that trigger a retry
        :return: The result of the function execution
    """

    def func_wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(func, *args, **kwargs)
                        result = future.result(timeout=timeout)
                        return result
                except concurrent.futures.TimeoutError:
                    logger.warning(f"Function timed out after {timeout} seconds. Retrying...")
                except exceptions as e:
                    temp = min(start_sleep_time * (factor ** n), border_sleep_time)
                    sleep_time = temp / 2 + choice((0, temp / 2))
                    logger.warning(f"Error: {e}. Retrying in {sleep_time} seconds...")
                    sleep(sleep_time)
                    n += 1
                except Exception as e:
                    logger.error(f"Unhandled exception: {e}. No retry will be attempted.")
                    raise

        return inner

    return func_wrapper
