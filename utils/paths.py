import utils
import os
from pathlib import Path


def resource(relative_path):
    absolute_path = str(Path(utils.__file__)
                        .parent
                        .parent
                        .joinpath(f'resources/{relative_path}'))
    return os.path.abspath(absolute_path)
