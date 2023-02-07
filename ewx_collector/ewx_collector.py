"""Main module."""


import json, os,csv, warnings
from datetime import datetime
from multiweatherapi import multiweatherapi
from dotenv import load_dotenv

from .time_intervals import previous_fifteen_minute_period

load_dotenv()

def get_reading(station_type, station_config,
                start_datetime_str = None,
                end_datetime_str = None):
    
    if not start_datetime_str:
        # no start ?  Use the internval 15 minutees before present timee.  see module for details.  Ignore end time if it's sent
        start_datetime,end_datetime =  previous_fifteen_minute_period()
    else:
        start_datetime = datetime.fromisoformat(start_datetime_str)
        if not end_datetime_str:
            # no end time, make end time 15 minutes from stard time given.  
            end_datetime = start_datetime + timedelta(minutes= 15)
        else:
            end_datetime = datetime.fromisoformat(end_datetime_str)


    params = station_config
    params['start_datetime'] = start_datetime
    params['end_datetime'] = end_datetime
    params['tz'] = 'ET'

    try:
        mwapi_resp = multiweatherapi.get_reading(station_type, **params)
    except Exception as e:
        raise e

    # includes mwapi_resp.resp_raw, and mwapi_resp.resp_transformed

    return mwapi_resp


def get_readings(stations:dict,
                start_datetime_str:str = None,
                end_datetime_str:str = None):
    """get readings from a list of stations
    
    station: dictionary keyed on station_id, station_type and config
    
    """
    
    readings = {}
    for station in stations:
        mwapi_resp = get_reading(
                    station_type = station['station_type'], 
                    station_config = station['station_config'],
                    start_datetime_str = start_datetime_str,
                    end_datetime_str = end_datetime_str)

        readings[station['station_id']] =  { 
             'station_id' : station['station_id'], 'station_type' : station['station_type'],
             'start': start_datetime_str,
             'end':end_datetime_str,
             'json' : mwapi_resp.resp_raw,
             'data' :  mwapi_resp.resp_transformed
        }
            
    return(readings)

    
def stations_from_env():
    """ this is a temporary cludge to convert the old style dot env into new listing"""
    
    station_types = ['DAVIS', 'CAMPBELL', 'ONSET', 'RAINWISE', 'SPECTRUM', 'ZENTRA']
    stations_available  = [s for s in station_types if s.upper() in os.environ.keys()]
    stations = {}
    for station_name in stations_available:
        stations[station_name] = {
            "station_id"     : f"{station_name}_1",
            "station_type"   : station_name,
            "station_config" : json.loads(os.environ[station_name])
        }
        
    return stations


def stations_from_file(csv_file_path:str):
    """ given a csv file of stations, read them into standard format
    returns a dictionary of dictionaries, keyed on 'station ID'
    
    """
    station_field_names = ["station_id", "station_type", "station_config"]
    
    if not os.path.exists(csv_file_path): 
        warnings.warn(f"file not found {csv_file_path}")
        return None
    
    stations = {}
    with open(csv_file_path, "r") as csvfile:
        csvreader = csv.DictReader(csvfile,  fieldnames = station_field_names, delimiter=",", quotechar="'") # 
        header = next(csvreader)
        for row in csvreader:
            stations[row['station_id']] = row
    
    return stations    

## random python notes 
# to convert the dictionary of stations into a simple list
# station_list = [s for s in stations.values()]
#  to get the first row in the dict of dict (for testing )
# sd = stations[list(stations.keys())[0]]