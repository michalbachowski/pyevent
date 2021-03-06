#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


# monkey patch os.link to force using symlinks
import os
del os.link

setup(name='PyEvent',
    url='https://github.com/michalbachowski/pyevent',
    version='1.0.0',
    description='Python implementation of PHP`s (from Symfony Components) EventDispatcher',
    license='New BSD License',
    author='Michał Bachowski',
    author_email='michal@bachowski.pl',
    package_dir={'': 'src'},
    py_modules=['pyevent'],
    install_requires='PyPromise==1.1.2',
    dependency_links = ['http://github.com/michalbachowski/pypromise/archive/1.1.2.zip#egg=PyPromise-1.1.2'])
