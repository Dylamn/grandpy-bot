from typing import Union, Any
from flask import current_app as app


def base_path(relpath: str = ''):
    """Get the path to the base of the project.

    :param relpath: Relative path which will be appended to the base path.
    """
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


def config(key: Union[str, list] = None, default=None) -> Any:
    """Get the specified configuration value.

    :param key: The key to access a value.
    :param default: The default returned value if nothing is found.
    :return Any:
    """
    if key is None:
        return app.config

    return data_get(app.config, key, default)


def data_get(target: Union[dict, list], key: Union[str, list],
             default=None) -> Any:
    """Get an item from a list/dict using "dot" notation.

    :param target: Must be either a list or a dict.

    :param key: The path to the value with dot notation.
        Can be a list of key (strings).

    :param default: The default value if nothing is found.
    """
    key = key.split('.') if isinstance(key, str) else key

    if not isinstance(key, list):
        return target

    # head is the current key on which we'll access.
    # tail is the key(s) left which we haven't access already.
    head, *tail = key

    if isinstance(target, list) \
            and (head.isnumeric() and int(head) < len(target)):
        value = target[int(head)]
    elif isinstance(target, dict) and head in target:
        value = target[head]
    else:
        return default

    return data_get(value, tail, default) if tail else value
