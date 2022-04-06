from datapoint import Datapoint
from datetime import datetime
import formulas
import requests


LOCAL_URL = "http://localhost:8000/measurement/"
REMOTE_URL = ""

SENSOR_ID_DICT = {
    formulas.LOG : 2,
    formulas.STEERING_ANGLE: 1
}


def send_packet(data: Datapoint):
    """
    :param data:
    Sends the data via a POST request to the mercury-telemetry endpoint: http://"mercury-website-url"/measurement.
    See https://github.com/mercury-telemetry/mercury-telemetry/wiki/JSON-Messaging-Format for info on the JSON format
    """

    jsonbody = {
    "sensor_id": SENSOR_ID_DICT[data.sense_id],
    "values": dict(zip(data.series_names,data.outputs)),
    "date": datetime.now().isoformat(),
    }
    result = requests.post(LOCAL_URL, json = jsonbody)
    print(result)

def send_log(line):
    jsonbody = {
    "sensor_id": SENSOR_ID_DICT[formulas.LOG],
    "values": {"log" : line},
    "date": datetime.now().isoformat(),
    }
    result = requests.post(LOCAL_URL, json=jsonbody)
    print(result)


