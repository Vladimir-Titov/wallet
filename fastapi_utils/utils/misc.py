import re

RE_SNAKE_CASE = re.compile(r'((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


def camel_case_to_snake_case(value: str) -> str:
    return RE_SNAKE_CASE.sub(r'_\1', value).lower()
