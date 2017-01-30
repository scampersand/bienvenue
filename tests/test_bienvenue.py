from __future__ import absolute_import, unicode_literals

from functools import partial
import bienvenue


def test_module_exports():
    """
    Test that the bienvenue package exports the expected symbols
    """
    exports = filter(lambda k: not k.startswith('_'), dir(bienvenue))
    need = ['env', 'unprefix']
    assert all(n in exports for n in need)


def test_integration():
    """
    Super-simple integration test through the bienvenue imports,
    composing env and unprefix
    """
    ENV = {'FOO_X': '1'}
    env = partial(bienvenue.env, bienvenue.unprefix('FOO_', ENV))
    assert env('X', 'default') == '1'
