from datapoint import Datapoint
from datetime import datetime
import formulas
import requests
from concurrent.futures import ThreadPoolExecutor


LOCAL_URL = "http://localhost:8000/measurement/"
REMOTE_URL = "http://nyu-baja-telemetry.herokuapp.com/measurement/"

SENSOR_ID_DICT = {
    formulas.LOG : 2,
    formulas.STEERING_ANGLE: 1
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

        jsonbody = {
        "sensor_id": SENSOR_ID_DICT[data.sense_id],
        "values": dict(zip(data.series_names,data.outputs)),
        "date": datetime.now().isoformat(),
        }
        arg = [jsonbody]
        self.executor.submit(self.post, *arg)

    def send_log(self, line):
        jsonbody = {
        "sensor_id": SENSOR_ID_DICT[formulas.LOG],
        "values": {"log" : line},
        "date": datetime.now().isoformat(),
        }
        arg = [jsonbody]
        self.executor.submit(self.post, *arg)

    def post(self, jsonbody):
        print(requests.post(LOCAL_URL, json=jsonbody))



