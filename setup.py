#!/usr/bin/env python
from __future__ import unicode_literals

import os
from setuptools import setup, find_packages


try:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except IOError:
    README = ''

setup(
    name='redmine-wikijs-migrator',
    version='0.1.1',
    description='Migrate a redmine project to gitlab',
    long_description=README,
    author='Julian Cervino',
    author_email='jcerigl@gmail.com',
    license='GPL',
    url='https://github.com/juliancervino/redmine-wikijs-migrator',
    packages=find_packages(),
    install_requires=['pyyaml', 'requests', 'GitPython', 'pypandoc'],
    entry_points={
        'console_scripts': [
            'redmine2wikijs=redmine_wikijs_migrator.commands:main'
        ],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)