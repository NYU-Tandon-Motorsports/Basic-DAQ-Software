from datapoint import Datapoint
import sensor_ids
import pygame
import threading

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


class Driver_Telemetry_Dashboard:
    def __init__(self):
        pygame.init()

        size = width, height = 720, 480
        black = 0, 0, 0
        self.screen = pygame.display.set_mode(size)
        self.screen.fill(black)
        pygame.display.flip()




    def display_speed(self, speed):
        if ENABLE_7_SEG:
            display_right.number(int(speed))
        print("I am going " + str(speed) + " mph!")


    def display_steering(self, angle):
        print("I am steering at a " + str(angle) + " degree angle!")
        # TODO call method to display steering angle (if applicable)


    def display_x_accel(self, accel):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(str(int(accel)), 1, (255, 255, 0))
        self.screen.blit(label, (100,100))


    # TODO make functions for all of the quantities we want the driver to see during the race

    def send_data(self, data : Datapoint):
        lock = threading.Lock()
        if data.sense_id == sensor_ids.GPS_SPEED:
            self.display_speed(data.outputs[0])
        elif data.sense_id == sensor_ids.STEERING_ANGLE:
            self.display_steering(data.outputs[0])
        elif data.sense_id == sensor_ids.DOF9:
            self.display_x_accel(data.outputs[0])
        lock.acquire()
        pygame.display.flip()
        lock.release()
