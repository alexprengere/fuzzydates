==========
FuzzyDates
==========

Fuzzy datetime reading.

Examples
--------

Import the main function:

.. code-block:: python

    >>> from fuzzy_dates import load_date

Examples of fuzzy reading:

.. code-block:: python

    >>> load_date('-0600', '[-+]%H%M')
    datetime.datetime(1900, 1, 1, 6, 0)
    >>> load_date('2010/01:02', '%Y[/:]%M[/:]%d')
    datetime.datetime(2010, 1, 2, 0, 1)
    >>> load_date('2010/01:02', '%Y[/:]%M/%d')
    Traceback (most recent call last):
    ValueError: Could not match regexp

Examples of fuzzy reading for timedelta:

.. code-block:: python

    >>> load_date('-0600', '[-+]%H%M', delta=True)
    datetime.timedelta(0, 21600)

