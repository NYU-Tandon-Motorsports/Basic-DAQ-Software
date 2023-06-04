cd /home/pi/Desktop/NYU_Baja/Basic-DAQ-Software/
chmod +x serialsensor.py
export XAUTHORITY=~/.Xauthority
export DISPLAY=:0
xrandr -o inverted
sudo xset s off
sudo xset s noblank
xterm -hold -e 'nohup python3 -u serialsensor.py' &
#python3 serialsensor.py
