#!/usr/bin/env python

import sys
from setuptools import setup

if 'register' in sys.argv:
    raise Exception('I don\'t want to be on PyPI!')

setup(name='piu',
      description='paste.in.ua',
      version='0.2',
      author='Alexander Solovyov',
      author_email='alexander@solovyov.net',
      packages=['piu'],
      include_package_data=True,
      install_requires=['opster>=3.3.1',
                        'bottle==0.12.7',
                        'Pygments==1.6',
                        'tornado==3.1.1',
                        'jinja2==2.7.1',
                        'tnetstring==0.2.1'],
      entry_points='''
      [console_scripts]
      piud = piu:main.command
      '''
      )
