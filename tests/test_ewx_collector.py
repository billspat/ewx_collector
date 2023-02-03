#!/usr/bin/env python

"""Tests for `ewx_collector` package."""

import pytest, random, string

# this is in a sample test and may be removed
import bs4


from ewx_collector import ewx_collector

@pytest.fixture
def random_string():
    """pytest fixture returns a string"""

    length = 10
    letters = string.ascii_lowercase
    return(''.join(random.choice(letters) for i in range(length)))


@pytest.fixture
def sample_fixture_response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests
    return requests.get('https://github.com/')


def test_content(sample_fixture_response):
    """Sample pytest test function with the pytest fixture as an argument."""
    from bs4 import BeautifulSoup
    assert 'GitHub' in BeautifulSoup(sample_fixture_response.content).title.string


def test_get_reading(random_string):
    """test the main (stub) function in this package

    :param random_string: string, pytest fixture
    :type random_string: string
    """

    reading_data = ewx_collector.get_reading(station_id=random_string)
    assert len(reading_data) > 0
    assert isinstance(reading_data, str)
