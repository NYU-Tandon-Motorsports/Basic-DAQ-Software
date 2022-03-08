import serial
from datetime import datetime

SERIAL_ARDUINO_COUNT = 1
now=datetime.now()
serial_in = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# serial_in2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
log = open("serialdata_" + now.strftime("%m%d%Y_%H:%M:%S") + ".txt", "x")
for i in range (0,500):
    raw = serial_in.readline()
    output = ""
    try:
        output = raw.decode()
        output = output.strip()   # removing extra stuff from serial stream
        if output[0:3] == "///":
            output = ""            # nothing is printed
        if output[0:3] == "###":
            output = "INFO: " + output[3:]   # info
            print(output)
        elif output[0:3] == "!!!":
            output = "ERROR: " + output[3:]    # error
            print(output)
        elif output[0:3] == "$$$":
            data = output[3:]
            data = data.split(' ')  # MUST BE OF LENGTH 7
            if len(data) != 7:
                raise Exception("Invalid sensor data format")
            sense_id = int(data[0])
            name = data[1]
            num_outputs = int(data[2])
            series_names = data[3].split(',')
            outputs = [float(var) for var in data[4].split(',')]
            units = data[5].split(',')
            time = float(data[6])
            # TODO Send packet with this datapoint to the SQL server
        else:
            print(output)  # extra serial stuff
    except UnicodeDecodeError:  # serial decode didnt work
        output = raw
    if output != "":
        log.write(output + "\n")
serial_in.close()
log.close()
exit()
