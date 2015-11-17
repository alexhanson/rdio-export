#!/usr/bin/env python
from setuptools import setup

setup(
    name='rdio-export',
    version='0.0.1',
    url='https://github.com/alexhanson/rdio-export',
    license="ISC License",
    install_requires=[
        'Rdio==0.3.0',
    ],
    packages=[
        'rdioexport',
    ],
    scripts=[
        'rdio-export',
    ],
)
