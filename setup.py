#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'numpy>=1.11',
    #'fitsio>=0.9.10'
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(hazboun6): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pypsrfits',
    version='0.1.0',
    description="Python package for dealing with PSRFITS files.",
    long_description=readme + '\n\n' + history,
    author="Jeffrey S Hazboun",
    author_email='jeffrey.hazboun@gmail.com',
    url='https://github.com/hazboun6/pypsrfits',
    packages=find_packages(include=['pypsrfits']),
    entry_points={
        'console_scripts': [
            'pypsrfits=pypsrfits.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='pypsrfits',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
