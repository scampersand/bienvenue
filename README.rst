=========
bienvenue
=========

|PyPI| |Build Status| |Coverage Report|

Python module for reading config from environment for `12-factor apps <https://12factor.net/>`_.
Supports Python 3.3+

Rationale
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

Installation
------------

Install from PyPI_:

.. code:: sh

    pip install bienvenue

Usage
-----

Bienvenue provides the function ``make_env_reader`` which returns a new
function for accessing the environment. For example:

.. code:: python

    from bienvenue import make_env_reader

    env = make_env_reader(prefix='MY_')

    DEBUG = env('DEBUG', False)
    SECRET_KEY = env('SECRET_KEY', 'fallback-secret-for-dev')
    ALLOWED_HOSTS = env('ALLOWED_HOSTS', [])

The env reader looks for ``MY_DEBUG`` in ``os.environ``. If it's not there,
the default value ``False`` will be returned. However if it's found, then the
value there will be interpreted according to the type of the default, in this
case boolean. Common strings such as on/off, true/false and yes/no are
interpreted into ``True`` or ``False``.

Likewise ``SECRET_KEY`` will be extracted from ``MY_SECRET_KEY`` and then
interpreted as a string value.

``ALLOWED_HOSTS`` will be extracted from ``MY_ALLOWED_HOSTS`` and JSON
decoded as a list, since the default value is a list.

If bienvenue encounters unknown types or values during parsing, it will log an
error and fall back to the provided default.

Legal
-----

Copyright 2017 `Scampersand LLC <https://scampersand.com>`_

Released under the `MIT license <https://github.com/scampersand/bienvenue/blob/master/LICENSE>`_

.. _PyPI: https://pypi.python.org/pypi/bienvenue

.. |Build Status| image:: https://img.shields.io/travis/scampersand/bienvenue/master.svg?style=plastic
   :target: https://travis-ci.org/scampersand/bienvenue?branch=master

.. |Coverage Report| image:: https://img.shields.io/codecov/c/github/scampersand/bienvenue/master.svg?style=plastic
   :target: https://codecov.io/gh/scampersand/bienvenue/branch/master

.. |PyPI| image:: https://img.shields.io/pypi/v/bienvenue.svg?style=plastic
   :target: PyPI_
