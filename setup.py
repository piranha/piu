#!/usr/bin/env python

import sys
from setuptools import setup

if 'register' in sys.argv:
    raise Exception('I don\'t want to be on PyPI!')

reqs = [x for x in
        open('requirements.txt').read().strip().splitlines()
        if not x.startswith('#')]

setup(name='piu',
      description='paste.in.ua',
      version='0.2',
      author='Alexander Solovyov',
      author_email='alexander@solovyov.net',
      license='ISC',
      packages=['piu'],
      include_package_data=True,
      install_requires=reqs,
      entry_points='''
      [console_scripts]
      piud = piu:main.command
      '''
      )
