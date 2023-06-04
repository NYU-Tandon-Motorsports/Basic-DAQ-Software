from datapoint import Datapoint
from datetime import datetime
import sensor_ids
import requests
import traceback
from concurrent.futures import ThreadPoolExecutor

ENABLE_TELEMETRY = False
LOCAL_URL = "http://localhost:8000/measurement/"
REMOTE_URL = "http://telemetry-nyubaja.herokuapp.com/measurement/"

SENSOR_ID_DICT = {   # maps the Basic daq software sensor id to that which the user assigns in Mercury
    sensor_ids.LOG : 2,
    sensor_ids.PIACCELEROMETER : 3,
    sensor_ids.GPS : 4,
    sensor_ids.GPS_SPEED : 8,
    sensor_ids.PIGYRO : 5,
    sensor_ids.ELECTRONICS_THERMOCOUPLE : 6,
    sensor_ids.DOF9 : 7,
    sensor_ids.STRING_POTENTIOMETER : 11,
    sensor_ids.CPUTEMP : 7,
    sensor_ids.HALL_EFFECT : 9,
    sensor_ids.HALL_EFFECT2 : 10,
    sensor_ids.SUS_ADC :  11
}

count = 500

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
        global count
        if count <= 0:
            return

        jsonbody = {
        "sensor_id": SENSOR_ID_DICT[data.sense_id],
        "values": dict(zip(data.series_names,data.outputs)),
        "date": datetime.now().isoformat(timespec='milliseconds'),
        }
        arg = [jsonbody]
        count -= 1
        self.executor.submit(self.post, *arg)

    def send_log(self, line):

        if ENABLE_TELEMETRY == False:
            return
        global count
        if count <= 0:
            return

        jsonbody = {
        "sensor_id": SENSOR_ID_DICT[sensor_ids.LOG],
        "values": {"log" : line},
        "date": datetime.now().isoformat(timespec='milliseconds'),
        }
        arg = [jsonbody]
        count -= 1
        self.executor.submit(self.post, *arg)

    def post(self, jsonbody):
        global count
        print(requests.post(REMOTE_URL, json=jsonbody, timeout = 5))
        count += 1

