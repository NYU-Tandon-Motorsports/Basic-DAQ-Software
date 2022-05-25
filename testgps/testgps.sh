killall gpsmon
killall gpsd
chmod +x testgps.py
python3 testgps.py
sudo gpsd /dev/ttyUSB1 -F /var/run/gpsd.sock
sudo gpsmon /dev/ttyUSB1
/bin/bash
