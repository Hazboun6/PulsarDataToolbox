#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'numpy>=1.11',
    'fitsio>=0.9.12',
    'six>=1.12.0',
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(Hazboun6): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest>=3.4.2',# TODO: put package test requirements here
]

setup(
    name='pdat',
    version='0.2.2',
    description="Python package for dealing with PSRFITS and other pulsar data files.",
    long_description=readme + '\n\n' + history,
    author="Jeffrey S Hazboun",
    author_email='jeffrey.hazboun@gmail.com',
    url='https://github.com/hazboun6/PulsarDataToolbox',
    packages=find_packages(include=['pdat']),
    include_package_data=True,
    package_data={'pdat': ['templates/*.fits']},
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords='pdat',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
