killall gpsmon
killall gpsd
chmod +x testgps.py
python3 testgps.py
RC=$?
sudo gpsd /dev/ttyUSB${RC} -F /var/run/gpsd.sock
sudo gpsmon /dev/ttyUSB${RC}
/bin/bash
