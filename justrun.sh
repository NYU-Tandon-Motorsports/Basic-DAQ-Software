chmod +x serialsensor.py
export XAUTHORITY=~/.Xauthority
export DISPLAY=:0
xset s 0 s blank
xrandr -o inverted
nohup python3 serialsensor.py &
#python3 serialsensor.py
