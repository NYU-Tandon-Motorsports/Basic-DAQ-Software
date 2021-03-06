from datapoint import Datapoint
from datetime import datetime
import sensor_ids
import requests
from concurrent.futures import ThreadPoolExecutor

ENABLE_TELEMETRY = True
LOCAL_URL = "http://localhost:8000/measurement/"
REMOTE_URL = "http://nyu-baja-telemetry.herokuapp.com/measurement/"

SENSOR_ID_DICT = {   # maps the Basic daq software sensor id to that which the user assigns in Mercury
    sensor_ids.LOG : 5,
    sensor_ids.GPS : 3,
    sensor_ids.GPS_SPEED : 4,
    sensor_ids.ELECTRONICS_THERMOCOUPLE : 6,
    sensor_ids.DOF9 : 7
}

class Pipeline:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=100)



    def send_packet(self, data: Datapoint):
        """
        :param data:
        Sends the data via a POST request to the mercury-telemetry endpoint: http://"mercury-website-url"/measurement.
        See https://github.com/mercury-telemetry/mercury-telemetry/wiki/JSON-Messaging-Format for info on the JSON format
        """
        if ENABLE_TELEMETRY == False:
            return
        jsonbody = {
        "sensor_id": SENSOR_ID_DICT[data.sense_id],
        "values": dict(zip(data.series_names,data.outputs)),
        "date": datetime.now().isoformat(timespec='milliseconds'),
        }
        arg = [jsonbody]
        self.executor.submit(self.post, *arg)

    def send_log(self, line):
        if ENABLE_TELEMETRY == False:
            return
        jsonbody = {
        "sensor_id": SENSOR_ID_DICT[sensor_ids.LOG],
        "values": {"log" : line},
        "date": datetime.now().isoformat(timespec='milliseconds'),
        }
        arg = [jsonbody]
        self.executor.submit(self.post, *arg)

    def post(self, jsonbody):
        print(requests.post(REMOTE_URL, json=jsonbody))

