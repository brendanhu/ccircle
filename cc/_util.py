from pathlib import Path


def hash_combine(seed, hashed):
    """ 'Adds' a hash to a seed, returning the new hash. """
    seed ^= hashed + 0x9e3779b9 + (seed << 6) + (seed >> 2)
    return seed


def get_ccircle_image_path(relative_path: str) -> Path:
    """ Get the pathlib.Path obj for the path relative to the ccircle directory.

    Params:
        relative_path: the path relative to the ccircle directory.

    TODO(Brendan): Throws an exception for file not found.
    """
    ccircle_dir = Path(__file__).resolve().parent.parent
    path = ccircle_dir.joinpath(relative_path)
    if not path.exists():
        raise RuntimeError(f'Image not found at {path}.')
    return path
