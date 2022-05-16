killall gpsmon
killall gpsd
sudo gpsd /dev/ttyUSB1 -F /var/run/gpsd.sock
gpsmon /dev/ttyUSB1
/bin/bash
