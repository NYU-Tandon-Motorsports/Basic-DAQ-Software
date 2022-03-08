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
        output = output.strip()

    except UnicodeDecodeError:
        output = raw
    log.write(output + "\n")
    print(output)

serial_in.close()
log.close()
exit()
