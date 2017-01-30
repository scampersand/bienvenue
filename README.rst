=========
bienvenue
=========

|PyPI| |Build Status| |Coverage Report|

Python module for reading config from environment for `12-factor apps <https://12factor.net/>`_.
Supports Python 2.7 and 3.3+

rationale
---------

In a 12-factor app, `config comes from the environment <https://12factor.net/config>`_.
For example, on Heroku, config variables are set using ``heroku config:set`` on the command line,
then `passed to the application in the environment <https://devcenter.heroku.com/articles/config-vars>`_.

Reading and parsing config from the environment is tedious and error-prone. For
example, a Django app has ``settings.DEBUG`` which should be
either ``True`` or ``False``. The operator runs ``heroku config:set DJANGO_DEBUG
off`` intending to disable it, but the application only sees a non-empty string
and treats the value as ``True``.

This sort of problem can be handled case-by-case but doesn't need to be. Clearly
a configuration setting with a fallback boolean value should be interpreted as
boolean from the environment. Likewise a fallback integer setting indicates the
associated environment variable should be converted from string to int.

Sounds like a job for a small and well-tested Python module, right?

installation
------------

Install from PyPI_:

.. code:: sh

    pip install bienvenue

usage
-----

Bienvenue provides two major functions: ``unprefix`` and ``env``. The former is
a simple filter to remove a common prefix from the keys in a dictionary. The
latter provides a similar interface as ``os.environ.get``, that is a getter with
fallback to a default, except that the default is required and provides type
hinting for decoding the string value.

Here's a snippet for your Django ``settings.py``:

.. code:: python

    from functools import partial
    import os
    import bienvenue

    env = partial(bienvenue.env, bienvenue.unprefix('DJANGO_', os.environ))

Now environment settings can be extracted as follows:

.. code:: python

    DEBUG = env('DEBUG', True)
    SECRET_KEY = env('SECRET_KEY', 'fallback-secret-for-dev')
    ALLOWED_HOSTS = env('ALLOWED_HOSTS', [])

In this example, ``DEBUG`` will be extracted from the environment variable
``DJANGO_DEBUG`` (because of calling ``bienvenue.unprefix`` above) and then
interpreted as a boolean value, honoring common strings such as on/off,
true/false, and yes/no.

Likewise ``SECRET_KEY`` will be extracted from ``DJANGO_SECRET_KEY`` and then
interpreted as a string value.

``ALLOWED_HOSTS`` will be extracted from ``DJANGO_ALLOWED_HOSTS`` and JSON
decoded as a list, since the default value is a list.

If bienvenue encounters unknown types or values during parsing, it will log an
error and fall back to the provided default.

legal
-----

Copyright 2017 Scampersand LLC

Released under the `MIT license <https://github.com/scampersand/bienvenue/blob/master/LICENSE>`_

.. _PyPI: https://pypi.python.org/pypi/bienvenue

.. |Build Status| image:: https://img.shields.io/travis/scampersand/bienvenue/master.svg?style=plastic
   :target: https://travis-ci.org/scampersand/bienvenue?branch=master

.. |Coverage Report| image:: https://img.shields.io/codecov/c/github/scampersand/bienvenue/master.svg?style=plastic
   :target: https://codecov.io/gh/scampersand/bienvenue/branch/master

.. |PyPI| image:: https://img.shields.io/pypi/v/bienvenue.svg?style=plastic
   :target: PyPI_
