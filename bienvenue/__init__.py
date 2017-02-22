from functools import partial
import os
from .env import env_get
from .unprefix import unprefix


def make_env_reader(d=os.environ, prefix=None, all=False, **kwargs):
    """
    Make a function that accesses a dict-like object, removing key prefixes and
    converting string values to types. Defaults to ``os.environ`` with no
    prefix.
    """
    if prefix:
        d = unprefix(prefix, d, all=all)
    return partial(env_get, d, **kwargs)
