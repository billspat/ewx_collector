#!/usr/bin/env python

import pytest, datetime


from ewx_collector import time_intervals


@pytest.fixture
def test_timestamp():
    """return a random timestamp, but just now for now"""
    return datetime.datetime.now(datetime.timezone.utc)


def test_15minutemark(test_timestamp):
    """test that we get something always on 15 minutes"""

    # no args
    dtm = time_intervals.fifteen_minute_mark()
    assert dtm.minute % 15 == 0

    # with args
    dtm = time_intervals.fifteen_minute_mark(test_timestamp)
    assert dtm.minute % 15 == 0

    just_past_two = datetime.datetime(2022,1,1,hour=2, minute=1, second=0)
    two = datetime.datetime(2022,1,1,hour=2, minute=0, second=0)
    assert time_intervals.fifteen_minute_mark(just_past_two) == two

    time_with_seconds  = datetime.datetime(2022,1,1,hour=2, minute=1, second=10)
    assert time_intervals.fifteen_minute_mark(time_with_seconds) == two
    


def test_previous_fifteen_minute_period():

    
    pfmp = time_intervals.previous_fifteen_minute_period()
    assert len(pfmp) == 2
    assert pfmp[1] > pfmp[0]
    assert pfmp[0].minute % 15 == 0
    assert pfmp[1].minute % 15 == 0
    assert  abs(pfmp[1].minute - pfmp[0].minute) == 15

    now = datetime.datetime.now(datetime.timezone.utc)
    pfmp = time_intervals.previous_fifteen_minute_period(now)
    assert pfmp[1] <= now
    assert now - pfmp[0] > datetime.timedelta(minutes=15)
    
    #TODO test that it's ac
    
    sample_dt = datetime.datetime(2022,1,1,hour=2, minute=10, second=0)
    pfmp = time_intervals.previous_fifteen_minute_period(sample_dt)
    assert pfmp[1] == datetime.datetime(2022,1,1,hour=2, minute=0, second=0)
    assert pfmp[0] == datetime.datetime(2022,1,1,hour=1, minute=45, second=0)
