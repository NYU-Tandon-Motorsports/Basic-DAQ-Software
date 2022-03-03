import serial
from datetime import datetime

now=datetime.now()
serial_in = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
file = open("accelerometer_" + now.strftime("%m%d%Y_%H:%M:%S") + ".txt", "x")
for i in range (0,500):
    raw = serial_in.readline()
    output = ""
    try:
        output = raw.decode()
        output = output.strip()
    except UnicodeDecodeError:
        output = raw
    file.write(output + "\n")
    print(output)

serial_in.close()
file.close()
exit()