#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module is the main launcher for tests.
"""

import unittest
import doctest

import fuzzy_dates


def test_suite():
    tests = unittest.TestSuite()

    # Standard options for DocTests
    opt = (doctest.ELLIPSIS |
           doctest.NORMALIZE_WHITESPACE |
           doctest.REPORT_ONLY_FIRST_FAILURE |
           doctest.IGNORE_EXCEPTION_DETAIL)

    tests.addTests(doctest.DocTestSuite(fuzzy_dates, optionflags=opt))
    tests.addTests(doctest.DocFileSuite('./README.rst'))

    return unittest.TestSuite(tests)


if __name__ == "__main__":
    # Verbosity is not available for some old unittest version
    # unittest.main(defaultTest='test_suite', verbosity=2)
    unittest.main(defaultTest='test_suite')
