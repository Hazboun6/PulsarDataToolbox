#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `PulsarDataToolbox` package."""


import unittest
import pytest

from pdat import pdat


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

# class TestPulsarDataToolbox(unittest.TestCase):
#     """Tests for `PulsarDataToolbox` package."""
#
#     def setUp(self):
#         """Set up test fixtures, if any."""
#
#     def tearDown(self):
#         """Tear down test fixtures, if any."""
#
#     def test_000_something(self):
#         """Test something."""
