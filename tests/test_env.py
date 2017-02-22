import pytest
from bienvenue.env import env_get


def test_bool_true():
    """
    specific string values are interpreted as True
    """
    for value in ['1', 'on', 't', 'true', 'y', 'yes']:
        assert env_get({'X': value}, 'X', False) == True


def test_bool_false():
    """
    specific string values are interpreted as False
    """
    for value in ['0', 'off', 'f', 'false', 'n', 'no']:
        assert env_get({'X': value}, 'X', True) == False


def test_bool_bool():
    """
    bool type is unexpected as value but handled
    """
    assert env_get({'X': False}, 'X', True) == False
    assert env_get({'X': True}, 'X', False) == True


def test_bool_type():
    """
    bool type as default implies required
    """
    assert env_get({'X': 'no'}, 'X', bool) == False
    assert env_get({'X': 'yes'}, 'X', bool) == True
    with pytest.raises(KeyError):
        env_get({}, 'X', bool)


def test_bool_missing():
    """
    missing key falls back to default value
    """
    assert env_get({}, 'X', False) == False
    assert env_get({}, 'X', True) == True


def test_bool_unknown():
    """
    unknown values raise an exception
    """
    for index, value in enumerate(['', '2', 'huh?', None], 1):
        with pytest.raises(ValueError):
            env_get({'X': value}, 'X', False)


def test_int():
    """
    digit strings are interpreted as int
    """
    assert env_get({'X': '0'}, 'X', 1) == 0
    assert env_get({'X': '1'}, 'X', 0) == 1
    assert env_get({'X': '42'}, 'X', 100) == 42


def test_int_int():
    """
    int type is unexpected as value but handled
    """
    assert env_get({'X': 42}, 'X', 1) == 42


def test_int_type():
    """
    int type as default implies required
    """
    assert env_get({'X': '42'}, 'X', int) == 42
    with pytest.raises(KeyError):
        env_get({}, 'X', int)


def test_int_default():
    """
    missing key falls back to default value
    """
    assert env_get({}, 'X', 42) == 42


def test_int_unknown():
    """
    unknown values raise exceptions
    """
    with pytest.raises(ValueError):
        env_get({'X': ''}, 'X', 42)
    with pytest.raises(ValueError):
        env_get({'X': 'whoops'}, 'X', 42)
    with pytest.raises(ValueError):
        env_get({'X': None}, 'X', 42)


def test_list():
    """
    JSON list is interpreted as list
    """
    assert env_get({'X': '[1]'}, 'X', []) == [1]


def test_list_list():
    """
    list type is unexpected but handled
    """
    assert env_get({'X': [1]}, 'X', []) == [1]


def test_list_type():
    """
    list type as default implies required
    """
    assert env_get({'X': '[1]'}, 'X', list) == [1]
    with pytest.raises(KeyError):
        env_get({}, 'X', list)


def test_list_default():
    """
    missing key falls back to default value
    """
    assert env_get({}, 'X', [1]) == [1]


def test_list_unknown():
    """
    unknown values and JSON failures raise exceptions
    """
    with pytest.raises(ValueError):
        env_get({'X': ''}, 'X', [1])
    with pytest.raises(ValueError):
        env_get({'X': 'whoops'}, 'X', [1])
    with pytest.raises(ValueError):  # json.JSONDecodeError
        env_get({'X': '[whoops]'}, 'X', [1])
    with pytest.raises(ValueError):
        env_get({'X': '{"foo": 1}'}, 'X', [1])
    with pytest.raises(ValueError):
        env_get({'X': {"foo": 1}}, 'X', [1])


def test_dict():
    """
    JSON object is interpreted as dict
    """
    assert env_get({'X': '{"foo": 1}'}, 'X', {}) == {"foo": 1}


def test_dict_dict():
    """
    dict type is unexpected but handled
    """
    assert env_get({'X': {"foo": 1}}, 'X', {}) == {"foo": 1}


def test_dict_type():
    """
    dict type as default implies required
    """
    assert env_get({'X': '{"foo": 1}'}, 'X', dict) == {"foo": 1}
    with pytest.raises(KeyError):
        env_get({}, 'X', dict)


def test_dict_default():
    """
    missing key falls back to default value
    """
    assert env_get({}, 'X', {"foo": 1}) == {"foo": 1}


def test_dict_unknown():
    """
    unknown values and JSON failures raise exceptions
    """
    with pytest.raises(ValueError):
        env_get({'X': ''}, 'X', {"foo": 1})
    with pytest.raises(ValueError):
        env_get({'X': 'whoops'}, 'X', {"foo": 1})
    with pytest.raises(ValueError):  # json.JSONDecodeError
        env_get({'X': '{1}'}, 'X', {"foo": 1})
    with pytest.raises(ValueError):
        env_get({'X': '[1]'}, 'X', {"foo": 1})
    with pytest.raises(ValueError):
        env_get({'X': [1]}, 'X', {"foo": 1})


def test_none():
    """
    with default=None, any value is passed through
    """
    o = object()
    assert env_get({'X': o}, 'X', None) is o


def test_unknown_value():
    """
    value with unknown type can't be converted
    """
    o = object()
    with pytest.raises(ValueError):
        env_get({'X': o}, 'X', 42)


def test_unknown_default():
    """
    default with unknown type can't be converted
    """
    o = object()
    with pytest.raises(ValueError):
        env_get({'X': '1'}, 'X', o)


def test_unknown_default_type():
    """
    default of unknown type can't be converted
    """
    with pytest.raises(ValueError):
        env_get({'X': '1'}, 'X', object)


def test_required():
    """
    required=True raises KeyError
    """
    assert env_get({'X': 1}, 'X', 0, required=True) == 1
    with pytest.raises(KeyError):
        env_get({}, 'X', 1, required=True)
