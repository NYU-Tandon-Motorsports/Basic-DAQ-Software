import serial
import time
print("INFO: Connecting GPS Port..")
try:
    serw = serial.Serial("/dev/ttyUSB2", baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
    serw.write('AT+QGPS=1\r'.encode())
    serw.close()
    time.sleep(1)
except Exception as e:
    print("ERROR: Serial port connection failed.")
    print(e)
exit(0)
