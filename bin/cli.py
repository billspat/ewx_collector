#!/usr/bin/env python
"""Console script for ewx_collector."""
import argparse
import sys, os

import ewx_collector

def main():
    """Console script for ewx_collector."""
    parser = argparse.ArgumentParser()
    parser.add_argument('csvfile', required=True, help="CSV file of stations with configuration")
    parser.add_argument('-s', '--start')
    parser.add_argument('-e', '--end')

    args = parser.parse_args()

    csvfile = args.file
    if os.path.exists(csvfile):
        # try
        stations =  ewx_collector.ewx_collector.stations_from_file(csvfile)
    else:
        print("file not found {csvfile}")
        return(1)
    
    # get recent data for now (ignore start and end times)
    weather_data = ewx_collector.ewx_collector.get_readings(stations)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
