from __future__ import absolute_import, unicode_literals

import logging
from .decoders import decoders


logger = logging.getLogger(__name__)


def env(d, key, default, decoders=decoders):
    """
    Look up ``key`` in ``d`` and decode it, or return ``default``.
    """
    try:
        value = d[key]
    except KeyError:
        return default
    for decoder in decoders:
        if (decoder.decodes_to_type(default) and
            decoder.decodes_from_type(value)
        ):
            try:
                return decoder.decode(value)
            except Exception as e:
                logger.error("%s couldn't convert %s=%r: %s: %s",
                             decoder.__class__.__name__,
                             key, value, e.__class__.__name__, e)
                return default
    logger.error("no env decoder for %s=%r (default=%r)", key, value, default)
    return default


__all__ = ['env']
