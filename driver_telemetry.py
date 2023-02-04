from datapoint import Datapoint
import sensor_ids
import pygame
import time
import threading
from concurrent.futures import ThreadPoolExecutor


ENABLE_DISPLAY = False




if ENABLE_DISPLAY:
    try:
        import tm1637
    except Exception as e:
        print("You are not using a Raspberry PI. Please make sure ENABLE_7_SEG is False.")
#This module will be used to call methods which display stuff on the Driver HUD. We can also do some calculations in here such as deriving new quantities and displaying them.
#One thing we must note is this is specifically for the offline stuff. If you are looking to fix data sent to the pits, see mercury-telemetry

## others will defined with different identification

"""
data: [(int ID), (string Name), (int num_outputs), (list<string> comsma_series_names), (list<double> comma_delimited outputs), (list<string> comma_delimited_units), (double time)]
"""

## Each method other than send_data will be

ENABLE_7_SEG = False
display_left = tm1637.TM1637(clk = 17, dio = 4) if ENABLE_7_SEG else None
display_right = tm1637.TM1637(clk = 16, dio = 21) if ENABLE_7_SEG else None

executor = ThreadPoolExecutor(max_workers=1)


#car states
accel_state = 0

def init_driver_telem():
    print("Starting PyGame")
    executor.submit(pygame_task)





def send_data(data : Datapoint):
    if data.sense_id == sensor_ids.DOF9:
        global accel_state
        accel_state = data.outputs[0]



def pygame_task():
    pygame.init()
    size = width, height = 720, 480
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    time.sleep(0.5)
    while(True):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(str(int(accel_state)), 1, (255, 255, 0))
        screen.fill(black)
        screen.blit(label, (100, 100))
        pygame.display.flip()
        time.sleep(0.5)