def hash_combine(seed, hashed):
    """ 'Adds' a hash to a seed, returning the new hash. """
    seed ^= hashed + 0x9e3779b9 + (seed << 6) + (seed >> 2)
    return seed



