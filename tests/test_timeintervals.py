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
