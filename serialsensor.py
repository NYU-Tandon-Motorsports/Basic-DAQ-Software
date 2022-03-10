import serial
from datetime import datetime

SERIAL_ARDUINO_COUNT = 1  # hard coded value for now will determine how many arduinos there are


def parse_serial(serial_in):
    raw = serial_in.readline()
    output = ""
    try:  # the try block is here because the serial stream can sometimes have extraneous bytes that cant be converted to plain text such as 00, 0A, etc.
        output = raw.decode()  # decode the binary stream
        output = output.strip()  # removing extra spaces and LFs from serial stream
        if output[0:3] == "///":  # Checking for three character signature in the beginning of each serial line to tell the parser what the purpose of the input is
            output = ""  # nothing is printed
        elif output[0:3] == "###":
            output = "INFO: " + output[3:]  # info
            print(output)
        elif output[0:3] == "!!!":
            output = "ERROR: " + output[3:]  # error
            print(output)
        elif output[0:3] == "$$$":
            data = output[3:]
            data = data.split(' ')  # MUST BE OF LENGTH 7. It is essentially being treated as a struct with 7 fields
            if len(data) != 7:
                raise Exception(output + " is in incorrect format. There must be 7 space-delimited elements (see sensorformat.txt).")
            sense_id = int(data[0])  # see sensorformat.txt for info on format for serial stream
            name = data[1]
            num_outputs = int(data[2])
            series_names = data[3].split(',')  # splits comma delimited vector inputs
            outputs = [float(var) for var in data[4].split(',')]  # splits comma delimited vector inputs and converts the values from string to float
            units = data[5].split(',')
            time = float(data[6])
            output = name + " ID = " + str(sense_id) + " " + str(series_names) + " " + str(outputs) + " " + str(units) + " t = " + str(time) + "s"  # logged output
            print(output)
            # TODO Send packet with these datapoints to the SQL server
        else:
            print(output)  # unmarked serial input
    except UnicodeDecodeError:  # serial decode didnt work
        output = ""
    return output


def main():
    now = datetime.now()
    log = open("serialdata_" + now.strftime("%m%d%Y_%H-%M-%S") + ".txt", "x")  # timestamping the text file and making a new log
    ## serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    serial_inputs = [serial.Serial('/dev/ttyUSB' + str(i)) for i in range(SERIAL_ARDUINO_COUNT)]  # creates SERIAL_ARDUINO_COUNT serial inputs
    """Each serial in represents an arduino plugged in VIA USB. Each arduino requires a separate serial instance"""
    # serial_in2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    for i in range(0, 500):
        for serial_in in serial_inputs:
            output = parse_serial(serial_in)
            if output != "":
                log.write(output + "\n")
    for serial_in in serial_inputs:
        serial_in.close()
    log.close()
    exit()

main()
