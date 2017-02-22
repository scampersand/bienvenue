def unprefix(prefix, d, all=False):
    """
    Returns a new dict by removing ``prefix`` from keys.
    If ``all`` is ``False`` (default) then drops keys without the prefix,
    otherwise keeping them.
    """
    d1 = dict(d) if all else {}
    d1.update((k[len(prefix):], v) for k, v in d.items() if k.startswith(prefix))
    return d1
