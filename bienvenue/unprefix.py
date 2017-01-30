from __future__ import absolute_import, print_function, unicode_literals


def unprefix(prefix, d, all=False):
    return dict((_unprefix_key(prefix, k), v) for k, v in d.items()
                if all or k.startswith(prefix))


def _unprefix_key(prefix, k):
    return k[len(prefix):] if k.startswith(prefix) else k


__all__ = ['unprefix']
