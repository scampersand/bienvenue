import abc
import json


class EnvDecoder:
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
        return self.to_types + (str,)

    def decodes_to_type(self, type):
        """
        Test if decoder can decode to type
        """
        return type in self.to_types

    def decodes_from_value(self, value):
        """
        Test if decoder can decode from value
        """
        return isinstance(value, self.from_types)

    def decode(self, value):
        """
        Decode the given value. Raises ValueError if type(value) isn't handled.
        """
        if isinstance(value, self.to_types):
            return value
        if isinstance(value, str):
            return self.from_string(value)
        raise ValueError("don't know {}".format(type(value)))  # pragma: no cover

    @abc.abstractmethod
    def from_string(self, s):
        """
        Decode from string ``s``, or raise an exception on failure.
        Must be overridden by subclass, and don't call super()
        """
        raise AssertionError("EnvDecoder.from_string shouldn't be called!")  # pragma: no cover


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

    to_types = (str,)

    def from_string(self, s):
        # never actually called, because EnvDecoder.decode short circuits since
        # the input type matches the output type.
        return s  # pragma: no cover


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

    def decodes_from_value(self, value):
        return isinstance(value, self.to_types) or (
            isinstance(value, str) and
            value.lstrip().startswith('[')
        )

    def from_string(self, s):
        return json.loads(s)


class EnvDict(EnvDecoder):
    """
    Decoder for JSON-encoded dicts.
    """

    to_types = (dict,)

    def decodes_from_value(self, value):
        return isinstance(value, self.to_types) or (
            isinstance(value, str) and
            value.lstrip().startswith('{')
        )

    def from_string(self, s):
        return json.loads(s)


class EnvNone(EnvDecoder):
    """
    Decode anything as a pass-through.
    """

    def decodes_to_type(self, type):
        return type is None

    def decodes_from_value(self, value):
        return True

    def decode(self, value):
        return value

    def from_string(self, s):
        raise AssertionError("EnvNone.from_string shouldn't be called!")  # pragma: no cover


decoders = [EnvBool(), EnvInt(), EnvList(), EnvDict(), EnvStr(), EnvNone()]


__all__ = ['env']
