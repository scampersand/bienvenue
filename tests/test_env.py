from __future__ import absolute_import, unicode_literals

from bienvenue.env import env


def test_bool_true():
    """
    specific string values are interpreted as True
    """
    for value in ['1', 'on', 't', 'true', 'y', 'yes']:
        assert env({'X': value}, 'X', False) == True


def test_bool_false():
    """
    specific string values are interpreted as False
    """
    for value in ['0', 'off', 'f', 'false', 'n', 'no']:
        assert env({'X': value}, 'X', True) == False


def test_bool_bool():
    """
    bool type is unexpected as value but handled
    """
    assert env({'X': False}, 'X', True) == False
    assert env({'X': True}, 'X', False) == True


def test_bool_missing(caplog):
    """
    missing key falls back to default value
    """
    assert env({}, 'X', False) == False
    assert env({}, 'X', True) == True
    assert len(caplog.records()) == 0


def test_bool_unknown(caplog):
    """
    unknown values fall back to default, after logging an error
    """
    assert len(caplog.records()) == 0
    for index, value in enumerate(['', '2', 'huh?', None], 1):
        assert env({'X': value}, 'X', False) == False
        assert len(caplog.records()) == (index - 1) * 2 + 1
        assert env({'X': value}, 'X', True) == True
        assert len(caplog.records()) == index * 2
    assert all(r.levelname == 'ERROR' for r in caplog.records())


def test_int():
    """
    digit strings are interpreted as int
    """
    assert env({'X': '0'}, 'X', 1) == 0
    assert env({'X': '1'}, 'X', 0) == 1
    assert env({'X': '42'}, 'X', 100) == 42


def test_int_int():
    """
    int type is unexpected as value but handled
    """
    assert env({'X': 42}, 'X', 1) == 42


def test_int_default(caplog):
    """
    missing key falls back to default value
    """
    assert env({}, 'X', 42) == 42
    assert len(caplog.records()) == 0


def test_int_unknown(caplog):
    """
    unknown values fall back to default, after logging an error
    """
    assert len(caplog.records()) == 0
    assert env({'X': ''}, 'X', 42) == 42
    assert env({'X': 'whoops'}, 'X', 42) == 42
    assert env({'X': None}, 'X', 42) == 42
    assert len(caplog.records()) == 3
    assert all(r.levelname == 'ERROR' for r in caplog.records())


def test_list():
    """
    JSON list is interpreted as list
    """
    assert env({'X': '[1]'}, 'X', []) == [1]


def test_list_list():
    """
    list type is unexpected but handled
    """
    assert env({'X': [1]}, 'X', []) == [1]


def test_list_default(caplog):
    """
    missing key falls back to default value
    """
    assert env({}, 'X', [1]) == [1]
    assert len(caplog.records()) == 0


def test_list_unknown(caplog):
    """
    unknown values and JSON failures fall back to default,
    after logging an error
    """
    assert len(caplog.records()) == 0
    assert env({'X': ''}, 'X', [1]) == [1]
    assert env({'X': 'whoops'}, 'X', [1]) == [1]
    assert env({'X': '[whoops]'}, 'X', [1]) == [1]
    assert env({'X': '{"foo": 1}'}, 'X', [1]) == [1]
    assert env({'X': {"foo": 1}}, 'X', [1]) == [1]
    assert len(caplog.records()) == 5
    assert all(r.levelname == 'ERROR' for r in caplog.records())


def test_dict():
    """
    JSON object is interpreted as dict
    """
    assert env({'X': '{"foo": 1}'}, 'X', {}) == {"foo": 1}


def test_dict_dict():
    """
    dict type is unexpected but handled
    """
    assert env({'X': {"foo": 1}}, 'X', {}) == {"foo": 1}


def test_dict_default(caplog):
    """
    missing key falls back to default value
    """
    assert env({}, 'X', {"foo": 1}) == {"foo": 1}
    assert len(caplog.records()) == 0


def test_dict_unknown(caplog):
    """
    unknown values and JSON failures fall back to default,
    after logging an error
    """
    assert len(caplog.records()) == 0
    assert env({'X': ''}, 'X', {"foo": 1}) == {"foo": 1}
    assert env({'X': 'whoops'}, 'X', {"foo": 1}) == {"foo": 1}
    assert env({'X': '{1}'}, 'X', {"foo": 1}) == {"foo": 1}
    assert env({'X': '[1]'}, 'X', {"foo": 1}) == {"foo": 1}
    assert env({'X': [1]}, 'X', {"foo": 1}) == {"foo": 1}
    assert len(caplog.records()) == 5
    assert all(r.levelname == 'ERROR' for r in caplog.records())


def test_none():
    """
    with default=None, any value is passed through
    """
    o = object()
    assert env({'X': o}, 'X', None) is o


def test_unknown_type(caplog):
    """
    unknown type can't be converted (except with default=None) and logs an
    error
    """
    assert len(caplog.records()) == 0
    o = object()
    assert env({'X': o}, 'X', 42) == 42
    assert len(caplog.records()) == 1
    assert all(r.levelname == 'ERROR' for r in caplog.records())
