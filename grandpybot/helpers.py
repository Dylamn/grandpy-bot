from typing import Union


def base_path(relpath: str = ''):
    """Get the path to the base of the project."""
    from pathlib import Path

    path = Path().absolute().resolve()
    project_dir = 'grandpy-bot'
    tries = 0

    if project_dir not in str(path):
        EnvironmentError('Project folder not found.')

    while not str(path).endswith(project_dir) and tries < 3:
        path = path.parent
        tries += 1

    return path.joinpath(relpath)


def data_get(d: dict, key: Union[str, list]):
    """Get an item from a dict using "dot" notation.

    :param d: A dictionnary.

    :param key: The path to the value with dot notation.
        Can be a list of key (strings).
    """
    key = key.split('.') if isinstance(key, str) else key

    # head is the current key on which we'll access.
    # tail is the key(s) left which we haven't access already.
    head, *tail = key

    value = d.get(head)

    return data_get(value, tail) if value and tail else value
