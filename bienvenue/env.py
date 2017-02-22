import logging
from .decoders import decoders
from .unprefix import unprefix


logger = logging.getLogger(__name__)


def env_get(d, key, default, decoders=decoders, required=None):
    """
    Look up ``key`` in ``d`` and decode it, or return ``default``.
    """
    if required is None:
        required = isinstance(default, type)

    try:
        value = d[key]
    except KeyError:
        if required:
            raise
        return default

    dt = (default if default is None or isinstance(default, type)
          else type(default))

    for decoder in decoders:
        if (decoder.decodes_to_type(dt) and
            decoder.decodes_from_value(value)
        ):
            try:
                return decoder.decode(value)
            except Exception as e:
                logger.error("%s couldn't convert %s: %s: %s",
                             decoder.__class__.__name__, key,
                             e.__class__.__name__, e)
                raise

    raise ValueError("no suitable env decoder for {}".format(key))
