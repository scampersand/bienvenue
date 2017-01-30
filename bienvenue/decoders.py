from __future__ import absolute_import, unicode_literals

import abc
import json


# Python 2/3 compatible definitions of string_types.
try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


class EnvDecoder(object):
    """
    Base class for type-specific decoders.
    """

    # This metaclass prevents this class from being instantiated, and
    # subclasses must override any abstract methods (``from_string``) before
    # they can be instantiated as well.
    __metaclass__ = abc.ABCMeta

    # resulting type(s) of decoding
    to_types = ()

    @property
    def from_types(self):
        """
        Types the decoder handles as input.
        Most decoders handle their output types plus strings.
        """
        return self.to_types + string_types

    def decodes_to_type(self, value):
        """
        Test if decoder can decode to type(value)
        """
        return isinstance(value, self.to_types)

    def decodes_from_type(self, value):
        """
        Test if decoder can decode from type(value)
        """
        return isinstance(value, self.from_types)

    def decode(self, value):
        """
        Decode the given value. Raises ValueError if type(value) isn't handled.
        """
        if isinstance(value, self.to_types):
            return value
        if isinstance(value, string_types):
            return self.from_string(value)
        raise ValueError("don't know {}".format(type(value)))

    @abc.abstractmethod
    def from_string(self, s):
        """
        Decode from string ``s``, or raise an exception on failure.
        Must be overridden by subclass, and don't call super()
        """
        raise AssertionError("EnvDecoder.from_string shouldn't be called!")


class EnvBool(EnvDecoder):
    """
    Decoder for boolean values. Handles various string representations of
    True/False.
    """

    to_types = (bool,)

    def from_string(self, s):
        s = s.lower()
        if s in ['1', 'on', 't', 'true', 'y', 'yes']:
            return True
        if s in ['0', 'off', 'f', 'false', 'n', 'no']:
            return False
        raise ValueError("can't interpret string as bool")


class EnvStr(EnvDecoder):
    """
    Decoder for string values. ``os.environ`` values should always be strings,
    so this is easy.
    """

    to_types = string_types

    def from_string(self, s):
        return s



class EnvInt(EnvDecoder):
    """
    Decoder for base 10 integer values.
    """

    to_types = (int,)

    def from_string(self, s):
        return int(s)


class EnvList(EnvDecoder):
    """
    Decoder for JSON-encoded lists.
    """

    to_types = (list,)

    def decodes_from_type(self, value):
        return isinstance(value, self.to_types) or (
            isinstance(value, string_types) and
            value.lstrip().startswith('[')
        )

    def from_string(self, s):
        return json.loads(s)


class EnvDict(EnvDecoder):
    """
    Decoder for JSON-encoded dicts.
    """

    to_types = (dict,)

    def decodes_from_type(self, value):
        return isinstance(value, self.to_types) or (
            isinstance(value, string_types) and
            value.lstrip().startswith('{')
        )

    def from_string(self, s):
        return json.loads(s)


class EnvNone(EnvDecoder):
    """
    Decode anything as a pass-through.
    """

    def decodes_to_type(self, value):
        return value is None

    def decodes_from_type(self, value):
        return True

    def decode(self, value):
        return value

    def from_string(self, s):
        raise AssertionError("EnvNone.from_string shouldn't be called!")


decoders = [EnvBool(), EnvInt(), EnvList(), EnvDict(), EnvStr(), EnvNone()]


__all__ = ['env']
