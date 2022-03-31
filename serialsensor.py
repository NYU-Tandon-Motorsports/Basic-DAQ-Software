import os
import serial
from datetime import datetime
import driver_telemetry
import datapoint
from formulas import Formulas
from datapoint import Datapoint
SERIAL_ARDUINO_COUNT = 1  # hard coded value for now will determine how many arduinos there are


def parse_serial(serial_in, formula_calc):
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
            data = datapoint.get_datapoint_from_arduino_raw(output)
            formula_calc.apply_calculation(data)
            output = str(data)
            print(output)
            driver_telemetry.send_data(data)
            # TODO Send packet with these datapoints to the SQL server
        else:
            print(output)  # unmarked serial input
    except UnicodeDecodeError:  # serial decode didnt work
        output = ""
    return output

def main():
    now = datetime.now()
    log = open(os.getcwd()+"/datalogs/serialdata_" + now.strftime("%m%d%Y_%H-%M-%S") + ".txt", "x")  # timestamping the text file and making a new log
    ## serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    log.write("Arduino data obtained from USB connection on " + now.strftime("%m/%d/%Y %H:%M:%S")+"\n\n")
    log.write("DAQ: Initializing " + str(SERIAL_ARDUINO_COUNT) + " Arduino(s)\n")
    print("DAQ: Initializing " + str(SERIAL_ARDUINO_COUNT) + " Arduino(s)")
    serial_inputs = [serial.Serial('/dev/ttyUSB' + str(i), 9600, timeout=1) for i in range(SERIAL_ARDUINO_COUNT)]  # creates SERIAL_ARDUINO_COUNT serial inputs
    log.write("DAQ: Successfully Initialized " + str(SERIAL_ARDUINO_COUNT) + " Arduino(s)\n")
    print("DAQ: Successfully Initialized " + str(SERIAL_ARDUINO_COUNT) + " Arduino(s)")
    """Each serial in represents an arduino plugged in VIA USB. Each arduino requires a separate serial instance"""
    # serial_in2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    formula_calc= Formulas()
    for i in range(0, 500): # Condition for when to stop the program
        for serial_in in serial_inputs:
            output = parse_serial(serial_in, formula_calc)
            if output != "" and output is not None and ord(output[0]) != 0:
                log.write(bytes(output, 'utf-8').decode('utf-8','ignore') + "\n")
    for serial_in in serial_inputs:
        serial_in.close()
    log.close()
    exit()

main()
