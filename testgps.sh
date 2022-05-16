killall gpsmon
killall gpsd
sudo gpsd /dev/ttyUSB1 -F /var/run/gpsd.sock
sudo gpsmon /dev/ttyUSB1
/bin/bash
