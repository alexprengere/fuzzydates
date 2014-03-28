#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module is the main launcher for tests.
"""

import unittest
import doctest

import os
import sys

# PYTHON PATH MANAGEMENT
DIRNAME = os.path.dirname(__file__)
if DIRNAME == '':
    DIRNAME = '.'

DIRNAME = os.path.realpath(DIRNAME)
UPDIR   = os.path.split(DIRNAME)[0]

if UPDIR not in sys.path:
    sys.path.append(UPDIR)

import fuzzy_dates



def test_suite():
    """
    Create a test suite of all doctests.
    """
    tests = unittest.TestSuite()

    # Standard options for DocTests
    opt =  (doctest.ELLIPSIS |
            doctest.NORMALIZE_WHITESPACE |
            doctest.REPORT_ONLY_FIRST_FAILURE |
            doctest.IGNORE_EXCEPTION_DETAIL)

    globs = {}

    tests.addTests(doctest.DocTestSuite(fuzzy_dates,
                                        optionflags=opt,
                                        extraglobs=globs))


    return unittest.TestSuite(tests)


if __name__ == "__main__":

    # Verbosity is not available for some old unittest version
    #unittest.main(defaultTest='test_suite', verbosity=2)
    unittest.main(defaultTest='test_suite')

