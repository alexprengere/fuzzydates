#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement

from setuptools import setup


with open('VERSION') as fl:
    VERSION = fl.read().rstrip()

with open('README.rst') as fl:
    LONG_DESCRIPTION = fl.read()

with open('LICENSE') as fl:
    LICENSE = fl.read()


setup(
    name='FuzzyDates',
    version=VERSION,
    author='Alex Prengère',
    author_email='alexprengere@gmail.com',
    url='https://github.com/alexprengere/fuzzydates',
    description='Fuzzy interpretation of dates.',
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    py_modules=[
        'fuzzy_dates'
    ],
)
