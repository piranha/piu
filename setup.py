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
      install_requires=['opster>=3.3.1', 'bottle>=0.9.6', 'pygments', 'tornado',
                        'jinja2', 'tnetstring'],
      entry_points='''
      [console_scripts]
      piud = piu:main.command
      '''
      )
