chmod +x serialsensor.py
control_c() {
    pkill -9 -f serialsensor.py
    exit
}

trap control_c SIGINT

while true ; do
   python3 serialsensor.py | while read line ; do
   echo $line
   ...
done
/bin/bash