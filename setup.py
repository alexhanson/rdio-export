#!/usr/bin/env python
from setuptools import setup

setup(
    name='rdio-export',
    version='0.0.1',
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
