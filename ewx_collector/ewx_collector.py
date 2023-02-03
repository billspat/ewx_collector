"""Main module."""


import json


def get_reading(station_id:str):
    """stub function to be implemented.  pull reading from a stations API with credentials"""
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

