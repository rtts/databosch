#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages

setup(
    name = 'databosch',
    version = '2.0',
    url = 'https://github.com/rtts/databosch',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    license = 'GPL3',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
)
