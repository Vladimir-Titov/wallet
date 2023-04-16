import random
import string


def proxy_args(*args, **kwargs):
    return args, kwargs


def random_string() -> str:
    return "".join(random.choices(string.ascii_letters, k=32))
