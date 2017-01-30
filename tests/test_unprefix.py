from __future__ import absolute_import, unicode_literals

from bienvenue.unprefix import unprefix


def test_empty_dict():
    """
    empty dict passes through
    """
    assert unprefix('PREFIX_', {}) == {}


def test_without_prefix():
    """
    keys without prefix are dropped
    """
    d = {'X': 1}
    d1 = unprefix('PREFIX_', d)
    assert d1 == {}
    assert d == {'X': 1}


def test_without_prefix_all():
    """
    keys without prefix are kept
    """
    d = {'X': 1}
    d2 = unprefix('PREFIX_', d, all=True)
    assert d2 == {'X': 1}
    assert d == {'X': 1}
    assert d2 is not d


def test_with_prefix():
    """
    keys with prefix are unprefixed
    """
    d = {'PREFIX_X': 1}
    d1 = unprefix('PREFIX_', d)
    assert d1 == {'X': 1}
    assert d == {'PREFIX_X': 1}


def test_with_prefix_all():
    """
    keys with prefix are unprefixed, original keys are kept
    """
    d = {'PREFIX_X': 1}
    d1 = unprefix('PREFIX_', d, all=True)
    assert d1 == {'X': 1, 'PREFIX_X': 1}
    assert d == {'PREFIX_X': 1}


def test_mixed():
    """
    mixed scenario dropping unprefixed keys
    """
    d = {'PREFIX_X': 1, 'Y': 2}
    d1 = unprefix('PREFIX_', d)
    assert d1 == {'X': 1}
    assert d == {'PREFIX_X': 1, 'Y': 2}


def test_mixed_all():
    """
    mixed scenario keeping unprefixed keys
    """
    d = {'PREFIX_X': 1, 'Y': 2}
    d1 = unprefix('PREFIX_', d, all=True)
    assert d1 == {'X': 1, 'Y': 2, 'PREFIX_X': 1}
    assert d == {'PREFIX_X': 1, 'Y': 2}
