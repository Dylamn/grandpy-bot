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
