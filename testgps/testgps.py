import serial
import time
from serial.tools import list_ports
print("INFO: Connecting GPS Port..")

device_signature= '2c7c:0125'
candidates=list(list_ports.grep(device_signature))
candidates.reverse()

print([candidate.device for candidate in candidates])

try:
    print("writing to "+ candidates[2].device)
    serw = serial.Serial(candidates[2].device, baudrate = 115200, timeout = 1,rtscts=True, dsrdtr=True)
    serw.write('AT+QGPS=1\r'.encode())
    serw.close()
    time.sleep(1)
except Exception as e:
    print("ERROR: Serial port connection failed.")
    print(e)
exit(int(candidates[1].device[-1]))
