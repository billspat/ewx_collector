"""Main module."""


import json, os
from datetime import datetime
import multiweatherapi
from dotenv import load_dotenv
from time_intervals import previous_fifteen_minute_period
load_dotenv()

def sample_reading():
    
    sample_reading = [
        {
            "station_id": "200000000500",
            "request_datetime": "2022-07-14 23:59:43",
            "data_datetime": "2022-07-14 22:00:00",
            "atemp": 18.6,
            "pcpn": 0.0,
            "relh": "71"
        }, 
        {
        "station_id": "200000000500",
        "request_datetime": "2022-07-14 23:59:43",
        "data_datetime": "2022-07-14 22:15:00",
        "atemp": 17.9,
        "pcpn": 0.0,
        "relh": "76"
        }
    ]
    
    return(json.dumps(sample_reading))



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
            "station_id" : f"{station_name}_1",
            "station_type" : station_name,
            "station_config" : os.environ[station_name]
        }
        
    return(stations)
