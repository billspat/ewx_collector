#!/usr/bin/env python

"""Tests for `ewx_collector` package."""

import pytest, random, string, os
from dotenv import load_dotenv
load_dotenv()


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
def sample_stations():
    stations = ewx_collector.stations_from_env()
    return(stations)

@pytest.fixture
def sample_fixture_response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    import requests
    return requests.get('https://github.com/')



def test_stations_from_env():
    stations = ewx_collector.stations_from_env()
    assert len(stations) > 0
    assert isinstance(stations, dict)
    assert 'DAVIS' in list(stations.keys())

def test_get_reading(sample_stations):
    station = sample_stations['DAVIS']
    reading = ewx_collector.get_reading(station['station_type'], 
                          station['station_config'],
                          start_datetime_str = None, 
                          end_datetime_str = None)
    
    assert reading is not None
    assert isinstance(reading.resp_raw, dict)
    assert len(reading.resp_raw) > 0 
    
    assert isinstance(reading.resp_transformed, list)
    assert len(reading.resp_transformed) > 0 
    assert isinstance(reading.resp_transformed[0], dict)
    
    assert isinstance(reading.resp_transformed[0], dict)
    
    # check that we got the keys we expect.  As the weather api grows this list will need to be updated
    # or built into the class/package
    expected_column_list = ['station_id', 'request_datetime', 'data_datetime', 'atemp', 'pcpn', 'relh']
    reading_fields = list(reading.resp_transformed[0].keys())
    
    assert reading_fields == expected_column_list
    
    
    

    
def test_content(sample_fixture_response):
    """Sample pytest test function with the pytest fixture as an argument."""
    from bs4 import BeautifulSoup
    assert 'GitHub' in BeautifulSoup(sample_fixture_response.content).title.string

