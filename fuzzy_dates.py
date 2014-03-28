#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Fuzzy datetime reading.

Examples of direct reading::

    >>> load_date('-0600', '-%H%M', verbose=1).strftime("%Y/%m/%d %Hh")
    [direct]
    '1900/01/01 06h'
    >>> load_date('-0600', '-%H%M', export=True, verbose=1)
    [direct]
    '1900-01-01 06:00:00'

Examples of fuzzy reading::

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

Examples of fuzzy reading for timedelta::

    >>> load_date('-0600', '[-+]%H%M', delta=True, verbose=0)
    datetime.timedelta(0, 21600)
    >>> load_date('-0600', '[-+]%H%M', delta=True, export=True, verbose=0)
    '6:00:00'

"""

from datetime import datetime
import re


# Frozen dictionaries :-)
DT_TO_RE = (
    ('%Y', '[0-9]{4}'),     # year         1999
    ('%y', '[0-9]{2}'),     # short year     99
    ('%m', '[01][0-9]'),    # month           3
    ('%d', '[0123][0-9]'),  # day
    ('%H', '[012][0-9]'),   # hour
    ('%M', '[0-6][0-9]'),   # minute
    ('%S', '[0-6][0-9]')    # second
)

RE_TO_NONGREEDY = (
    ('.*', '.*?'),
    ('.+', '.+?')
)


def load_date(fuzzy_date, pattern, delta=False, export=False, verbose=0):
    """
    Main function.

    :param fuzzy_date: the str containing a fuzzy date, meaning \
        we have a date probably mixed with other stuff
    :param pattern:    the pattern of the fuzzy_date. This can be \
        only standard datetime.strptime syntax, or it can be mixed \
        with other pattern from the re module
    :param delta:      if you want to get a timedelta object in return
    :param export:     if you want to have the result as a string format. \
        This argument is pretty useless, since it only performs a str() \
        at the end.
    :param verbose:    verbosity
    :returns:          a datetime object
    :raises:           ValueError, if the regexp could not match

    Examples of direct reading::

        >>> load_date('-0600', '-%H%M', verbose=1).strftime("%Y/%m/%d %Hh")
        [direct]
        '1900/01/01 06h'
        >>> load_date('-0600', '-%H%M', export=True, verbose=1)
        [direct]
        '1900-01-01 06:00:00'

    Examples of fuzzy reading::

        >>> load_date('-0600', '[-+]%H%M', verbose=1)
        [fuzzy]
        datetime.datetime(1900, 1, 1, 6, 0)
        >>> load_date('-0600', '[-+]%H%M', export=True, verbose=0)
        '1900-01-01 06:00:00'

    Examples of fuzzy reading for timedelta::

        >>> load_date('-0600', '[-+]%H%M', delta=True)
        datetime.timedelta(0, 21600)
        >>> load_date('-0600', '[-+]%H%M', delta=True, export=True)
        '6:00:00'

    Examples of errors::

        >>> load_date('2010/01:02', '%Y[/:]%M[/:]%d')
        datetime.datetime(2010, 1, 2, 0, 1)
        >>> load_date('2010/01:02', '%Y[/:]%M/%d')
        Traceback (most recent call last):
        ValueError: Could not match regexp
    """
    # We try simple date interpretation, if success --> else:
    try:
        dt = _load_date_direct(fuzzy_date, pattern, verbose=verbose)

    except ValueError:
        # We will perform fuzzy load later
        pass
    else:
        # Success: we return the datetime result
        return _export(dt, delta=delta, export=export)


    # If we are here, previous try failed,
    # so we try fuzzy interpretation
    try :
        dt = _load_date_fuzzy(fuzzy_date, pattern, verbose=verbose)

    except ValueError:
        raise ValueError('Could not match regexp')
    else:
        return _export(dt, delta=delta, export=export)


def _export(dt, delta=False, export=False):
    """
    Export function.

    >>> dt = datetime(1900, 1, 1, 6, 0)
    >>>
    >>> _export(dt, delta=False, export=False)
    datetime.datetime(1900, 1, 1, 6, 0)
    >>> _export(dt, delta=False, export=True)
    '1900-01-01 06:00:00'
    >>>
    >>> _export(dt, delta=True, export=False)
    datetime.timedelta(0, 21600)
    >>> _export(dt, delta=True, export=True)
    '6:00:00'
    """

    if delta:
        # BLUUUUUUUUUURP
        dt = dt - datetime.strptime('', '')

    if export:
        # NIIIICE
        return str(dt)

    return dt



def _load_date_direct(fuzzy_date, pattern, verbose=1):
    """
    Examples of direct reading::

        >>> _load_date_direct('-0600', '-%H%M').strftime("%Y/%m/%d %Hh")
        [direct]
        '1900/01/01 06h'

    Examples of fuzzy reading::

        >>> _load_date_direct('-0600', '[-+]%H%M')
        Traceback (most recent call last):
        ValueError: time data '-0600' does not match format '[-+]%H%M'

    """
    dt = datetime.strptime(fuzzy_date, pattern)

    if verbose:
        print '[direct]'

    return dt


def _load_date_fuzzy(fuzzy_date, pattern, verbose=1):
    """
    Examples of direct reading::

        >>> _load_date_fuzzy('-0600', '-%H%M').strftime("%Y/%m/%d %Hh")
        [fuzzy]
        '1900/01/01 06h'

    Examples of fuzzy reading::

        >>> _load_date_fuzzy('-0600', '[-+]%H%M')
        [fuzzy]
        datetime.datetime(1900, 1, 1, 6, 0)
        >>> _load_date_fuzzy('0600', '[-+]?%H%M')
        [fuzzy]
        datetime.datetime(1900, 1, 1, 6, 0)
    """
    match = re.match(_prepare_pattern(pattern), fuzzy_date)

    if match is None:
        raise ValueError()

    if verbose >= 2:
        print "%s -> %s" % (_prepare_pattern(pattern), match.groupdict())

    if verbose:
        print '[fuzzy]'

    return _match_to_dt(match.groupdict())


def _prepare_pattern(pattern):
    """
    Build full pattern.

    >>> _prepare_pattern('[-+]?%H%M')
    '[-+]?(?P<H>[012][0-9])(?P<M>[0-6][0-9])'
    """
    for dtsymb, reg in DT_TO_RE:
        pattern = pattern.replace(dtsymb, _label_group(dtsymb[1:], reg))

    for greg, ureg in RE_TO_NONGREEDY:
        pattern = pattern.replace(greg, ureg)

    return pattern


def _label_group(key, pattern):
    """
    Build the right pattern for matching with
    named entities.

    >>> _label_group('key', '[0-9]{4}')
    '(?P<key>[0-9]{4})'
    """
    return '(?P<%s>%s)' % (key, pattern)


def _match_to_dt(match):
    """
    Build a datetime from a dictionary of information.
    These infos were given by re.match.

    >>> _match_to_dt({'Y': '2010', 'm': None})
    datetime.datetime(2010, 1, 1, 0, 0)
    """
    if not match:
        # Case where empty dictionary of matching
        raise ValueError()

    smatch = [('%%%s' % k, m) for k, m in match.iteritems() if m is not None]

    return datetime.strptime('_'.join(t[1] for t in smatch), # date
                             '_'.join(t[0] for t in smatch)) # pattern



def _test():
    """
    Test on direct call.
    """

    import doctest

    optionflags = (
        doctest.NORMALIZE_WHITESPACE      |
        doctest.ELLIPSIS                  |
        doctest.REPORT_ONLY_FIRST_FAILURE |
        doctest.IGNORE_EXCEPTION_DETAIL
    )

    globs = {}

    doctest.testmod(optionflags=optionflags,
                    extraglobs=globs,
                    verbose=False)


if __name__ == '__main__':
    _test()

