==========
FuzzyDates
==========

Fuzzy datetime reading.

Examples
--------

Import the main function:

.. code-block:: python

    >>> from fuzzy_dates import load_date

Examples of direct reading:

.. code-block:: python

    >>> load_date('-0600', '-%H%M', verbose=1).strftime("%Y/%m/%d %Hh")
    [direct]
    '1900/01/01 06h'
    >>> load_date('-0600', '-%H%M', export=True, verbose=1)
    [direct]
    '1900-01-01 06:00:00'

Examples of fuzzy reading:

.. code-block:: python

    >>> load_date('-0600', '[-+]%H%M', verbose=1)
    [fuzzy]
    datetime.datetime(1900, 1, 1, 6, 0)
    >>> load_date('-0600', '[-+]%H%M', export=True)
    '1900-01-01 06:00:00'
    >>> load_date('2010/01:02', '%Y[/:]%M[/:]%d')
    datetime.datetime(2010, 1, 2, 0, 1)
    >>> load_date('2010/01:02', '%Y[/:]%M/%d')
    Traceback (most recent call last):
    ValueError: Could not match regexp

Examples of fuzzy reading for timedelta:

.. code-block:: python

    >>> load_date('-0600', '[-+]%H%M', delta=True, verbose=0)
    datetime.timedelta(0, 21600)
    >>> load_date('-0600', '[-+]%H%M', delta=True, export=True, verbose=0)
    '6:00:00'

