from __future__ import absolute_import, unicode_literals

from functools import partial
import os
import bienvenue
from bienvenue import make_env_reader


def test_module_exports():
    """
    Test that the bienvenue package exports the expected symbols.
    """
    exports = [k for k in dir(bienvenue) if not k.startswith('_')]
    need = ['make_env_reader', 'env_get', 'unprefix']
    assert all(n in exports for n in need)


def test_make_env_reader():
    """
    Integration test through make_env_reader which composes env_get and
    unprefix.
    """
    ENV = {'PREFIX_A': '1', 'A': '2', 'B': '3'}

    env = make_env_reader(ENV)
    assert env('PREFIX_A', 0) == 1
    assert env('A', 0) == 2
    assert env('B', 0) == 3

    env = make_env_reader(ENV, 'PREFIX_')
    assert env('PREFIX_A', 0) == 0
    assert env('A', 0) == 1
    assert env('B', 0) == 0

    env = make_env_reader(ENV, 'PREFIX_', all=True)
    assert env('PREFIX_A', 0) == 1
    assert env('A', 0) == 1  # important!
    assert env('B', 0) == 3


def test_make_env_reader_os_environ():
    """
    Test that make_env_reader uses os.environ by default
    """
    assert 'PREFIX_TESTING123' not in os.environ
    os.environ['PREFIX_TESTING123'] = 'it works'
    try:
        assert make_env_reader()('PREFIX_TESTING123', None) == 'it works'
        assert make_env_reader(prefix='PREFIX_')('TESTING123', None) == 'it works'
    finally:
        del os.environ['PREFIX_TESTING123']
