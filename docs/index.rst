googleoauth2django
==================

oauth2client is deprecated and there seems to be no path forward for poor souls who used the contrib/django_util code from it.

So I converted django_util into ``googleoauth2django`` to support Django >=2, Python 3.6, and google-auth-oauthlib.

Getting started
---------------

We recommend installing via ``pip``:

.. code-block:: bash

    $ pip install --upgrade googleoauth2django

You can also install from source:

.. code-block:: bash

    $ git clone https://github.com/google/googleoauth2django
    $ cd googleoauth2django
    $ python setup.py install


Library Documentation
---------------------

* Complete library index: :ref:`genindex`
* Index of all modules: :ref:`modindex`
* Search all documentation: :ref:`search`


Supported Python Versions
-------------------------

We support Python 3.4+. (Whatever this file says, the truth is
always represented by our `tox.ini`_).

.. _tox.ini: https://github.com/google/googleoauth2django/blob/master/tox.ini
