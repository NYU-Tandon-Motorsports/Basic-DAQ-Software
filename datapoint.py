class Datapoint:
    def __init__(self, sense_id, name, num_outputs, series_names, outputs, units, t):
        self.sense_id = sense_id
        self.name = name
        self.num_outputs = num_outputs
        self.series_names = series_names
        self.outputs = outputs
        self.units = units
        self.t = t

    def __repr__(self):
        pass

    def __str__(self):
        output = self.name + " ID = " + str(self.sense_id) + " " + str(self.series_names) + " " + str(
            self.outputs) + " " + str(self.units) + " t = " + str(self.t) + "s"  # logged output
        return output


def get_datapoint_from_arduino_raw(arduino_str):
    """
    Parses Arduino serial output according to sensorformat.txt. It is very important you follow this format in order for this to work properly
    :param arduino_str:
    :return: A new instance of Datapoint with the fields filled based on the arduino's output
    """
    data = arduino_str[3:]
    data = data.split(' ')  # MUST BE OF LENGTH 7. It is essentially being treated as a struct with 7 fields
    if len(data) != 7:
        raise Exception(
            arduino_str + " is in incorrect format. There must be 7 space-delimited elements (see sensorformat.txt).")
    sense_id = int(data[0])  # see sensorformat.txt for info on format for serial stream
    name = data[1]
    num_outputs = int(data[2])
    series_names = data[3].split(',')  # splits comma delimited vector inputs
    outputs = [float(var) for var in
               data[4].split(',')]  # splits comma delimited vector inputs and converts the values from string to float
    units = data[5].split(',')
    time = float(data[6])
    return Datapoint(sense_id, name, num_outputs, series_names, outputs, units, time)
