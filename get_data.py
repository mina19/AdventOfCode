import time
from functools import wraps
from typing import Any, Callable

import requests
import urllib3
from session import session

urllib3.disable_warnings()


def save_data(year=2025, day=1):
    urllib3.disable_warnings()
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    input_data = requests.get(url, cookies={"session": session}, verify=False).text

    f = open(f"{year}/{day}/day{day:02d}.txt", "w")
    f.write(input_data)
    f.close()
    return


def timeit(func: Callable) -> Callable:
    """
    A decorator that measures and prints the execution time of a function.

    Args:
        func: The function to be timed

    Returns:
        Wrapped function that prints execution time before returning the result
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time:.4f} seconds to execute")
        return result

    return wrapper
