#!/usr/bin/env python
"""Console script for ewx_collector."""
import argparse
import sys, os

import ewx_collector

def main():
    """Console script for ewx_collector."""
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', help="CSV file of stations with config")
    parser.add_argument('-s', '--start', help="start time UTC in format ")
    parser.add_argument('-e', '--end',help="end time UTC in format ")
    # parser.add_argument('_', nargs='*')

    args = parser.parse_args()

    csvfile = args.csvfile
    if os.path.exists(csvfile):
        # try
        stations =  ewx_collector.stations_from_file(csvfile)
        print(f"file has {len(stations)} stations")
    else:
        print("file not found {csvfile}")
        return(1)
    
    # get recent data for now (ignore start and end times)
    weather_data = ewx_collector.get_readings(stations)
    print(weather_data)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
