chmod +x serialsensor.py
export XAUTHORITY=~/.Xauthority
export DISPLAY=:0
xrandr -o inverted
python3 serialsensor.py
