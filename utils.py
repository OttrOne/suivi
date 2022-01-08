from string import ascii_uppercase, digits
from random import choice
from re import compile

def id_generator(length=8, chars=ascii_uppercase + digits):
    return ''.join(choice(chars) for _ in range(length))

def hrsize(num: int) -> str:
    for unit in ['', 'KiB', 'MiB', 'GiB', 'TiB']:
        if num < 1024.0:
            return f"{num:3.1f}{unit}"
        num /= 1024.0

def handle_variables(config: str, context: dict = {}) -> str:

    pattern = compile('.*?\${(\w+)}.*?')
    match = pattern.findall(config)

    if match:
        for var in match:
            if var in context:
                # leave var in config if not in context
                config = config.replace(f"${{{var}}}", context.get(var))

    return config
