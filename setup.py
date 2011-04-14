#!/usr/bin/env python

import sys
from setuptools import setup

if 'register' in sys.argv:
    raise Exception('I don\'t want to be on PyPI!')

setup(name='piu',
      description='paste.in.ua',
      version='0.1',
      author='Alexander Solovyov',
      author_email='piranha@piranha.org.ua',
      packages=['piu'],
      include_package_data=True,
      install_requires=['opster', 'bottle', 'redis', 'pygments', 'paste', 'jinja2', 'tnetstrings'],
      entry_points='''
      [console_scripts]
      piud = piu:main
      '''
      )
