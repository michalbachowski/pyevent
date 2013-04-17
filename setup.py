#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyEvent',\
    url='https://github.com/michalbachowski/pyevent',\
    version='1.0',\
    description='Python implementation of PHP`s (from Symfony Components) EventDispatcher',\
    license='New BSD License',\
    author='Michał Bachowski',\
    author_email='michal@bachowski.pl',\
    package_dir={'': 'src'},\
    packages=['pyevent'])
