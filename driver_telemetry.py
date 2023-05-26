from datapoint import Datapoint
import sensor_ids
import pygame
import time


import threading
from concurrent.futures import ThreadPoolExecutor
from math import pi, cos, sin
import RPi.GPIO as GPIO

ENABLE_DISPLAY = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PINK = (227, 0, 166)

THE_STRING = "MM" + ':' + "SS" + ':' + "MS"

WIDTH, HEIGHT = 800, 480
center = (510, HEIGHT / 2)
clock_radius = 200

if ENABLE_DISPLAY:
    try:
        import tm1637
    except Exception as e:
        print("You are not using a Raspberry PI. Please make sure ENABLE_7_SEG is False.")
# This module will be used to call methods which display stuff on the Driver HUD. We can also do some calculations in here such as deriving new quantities and displaying them.
# One thing we must note is this is specifically for the offline stuff. If you are looking to fix data sent to the pits, see mercury-telemetry

## others will defined with different identification

"""
data: [(int ID), (string Name), (int num_outputs), (list<string> comsma_series_names), (list<double> comma_delimited outputs), (list<string> comma_delimited_units), (double time)]
"""

## Each method other than send_data will be

ENABLE_7_SEG = False
display_left = tm1637.TM1637(clk=17, dio=4) if ENABLE_7_SEG else None
display_right = tm1637.TM1637(clk=16, dio=21) if ENABLE_7_SEG else None

executor = ThreadPoolExecutor(max_workers=1)

# car states
accel_state = 0
angle_state = 0
current_time = 0




def init_driver_telem():
    #try:
    #    GPIO.setmode(GPIO.BCM)
    #    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #    GPIO.add_event_detect(21, GPIO.RISING, callback=reset_timer)#
#
 #   finally:
 #       GPIO.cleanup()

    print("Starting PyGame")
    executor.submit(pygame_task)


def send_data(data: Datapoint):
    if data.sense_id == sensor_ids.STRING_POTENTIOMETER:
        global angle_state
        angle_state = data.outputs[0]


def pygame_task():
    # pygame stuff

    pygame.init()
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    clock = pygame.time.Clock()
    pygame.display.set_caption("Dashboard")

    while (True):
        #print("hello0")
        screen.fill(BLACK)
        #print("hello1")

        # SPEEDOMETER
        write_text(screen, "Speedometer", 30, (WIDTH / 4, (HEIGHT / 2) - (clock_radius / 2) - 60))
        #print("hello1.1")

        # clock outline
        #pygame.draw.circle(screen, WHITE, (WIDTH / 4, (HEIGHT / 2) + 45), clock_radius - 10, 10)
        # clock numbers
        #print("hello1.2")

        clock_nums(screen, 0, 8, 5, 40, (clock_radius - 65), 38.57143, 223.2, (WIDTH / 4), (HEIGHT / 2) + 45)
        # ticks
        ticks(screen, 0, 36, (clock_radius - 15), 7.714286, 223.2, WIDTH / 4, (HEIGHT / 2) + 45)
        # speed = myfont.render(str(int(MPH_state )), 1, (255, 255, 255))
        #
        #
        #
        speed = angle_state
        #print(speed)
        #speed=5
        #
        #
        #
        if (speed < 0):
            speed = 0
        if (speed > 35):
            speed = 35
        theta = (speed * (270 / 35.0)) + 223.2
        pygame.draw.line(screen, PINK, ((WIDTH / 2) / 2, HEIGHT / 2 + 45),
                         polar_to_cartesian(140, theta, WIDTH / 4, (HEIGHT / 2) + 45), 4)

        # RPM
        write_text(screen, "RPM Gauge", 30, ((WIDTH / 4) * 3, (HEIGHT / 2) - (clock_radius / 2) - 60))
        # gauge outline
        #pygame.draw.circle(screen, WHITE, ((WIDTH / 4) * 3, (HEIGHT / 2) + 45), clock_radius - 10, 10)
        circle_to_arc = 75
        # danger arc
        pygame.draw.arc(screen, PINK, (800, (((HEIGHT - (clock_radius * 2)) / 2) + (circle_to_arc / 2) + 100),
                                        ((clock_radius * 2) - circle_to_arc), ((clock_radius * 2) - circle_to_arc)),
                        5.5, 6.58, 5)
        # clock numbers
        clock_nums(screen, 1, 11, 1, 40, (clock_radius - 65), 30, 193.2, (WIDTH / 4) * 3, (HEIGHT / 2) + 45)
        # ticks
        ticks(screen, 0, 91, (clock_radius - 15), 3, 223.2, (WIDTH / 4) * 3, (HEIGHT / 2) + 45)
        # rpm = myfont.render(str(int(RPM_state)), 1, (255, 255, 255))
        rpm = 1
        theta = (rpm * (270 / 9)) + 193.2
        pygame.draw.line(screen, PINK, (((WIDTH / 4) * 3), (HEIGHT / 2) + 45),
                         polar_to_cartesian(140, theta, (WIDTH / 4) * 3, (HEIGHT / 2) + 45), 4)

        # TIMER
        # timer outline
        pygame.draw.rect(screen, PINK, [(WIDTH / 2) - (WIDTH / 7), HEIGHT / 40 - 10, WIDTH / (3.5), HEIGHT / 7], 5)
        start = pygame.time.get_ticks()
        render_time(screen, start, 50)
        #print("hello2")
        pygame.display.flip()
        clock.tick(60)


# pygame stuff
def write_text(screen, text, size, position):
    font = pygame.font.SysFont("Arial", size, True, False)
    text = font.render(text, True, WHITE)
    text_rect = text.get_rect(center=(position))
    screen.blit(text, text_rect)


def render_time(screen, start, size):
    hundredth_of_a_second = int(str(start)[-2:])  # hundredth of a second
    time_in_ms = time((start // 1000) // 3600, ((start // 1000) // 60 % 60), (start // 1000) % 60)
    time_string = "{}{}{:02d}".format(time_in_ms.strftime("%M:%S"), ':', hundredth_of_a_second)
    write_text(screen, time_string, size, (WIDTH / 2, HEIGHT / 13))



# theta is in degrees
def polar_to_cartesian(r, theta, width_center, height_center):
    x = r * sin(pi * theta / 180)
    y = r * cos(pi * theta / 180)
    return x + width_center, -(y - height_center)


def clock_nums(screen, rg_strt, rg_end, mult, size, r, angle, strt_angle, width_center, height_center):
    for number in range(rg_strt, rg_end):
        write_text(screen, str(number * mult), size,
                   polar_to_cartesian(r, (number * angle + strt_angle), width_center, height_center))


def ticks(screen, rg_strt, rg_end, r, angle, strt_angle, width_center, height_center):
    for number in range(rg_strt, rg_end):
        tick_start = polar_to_cartesian(r, (number * angle + strt_angle), width_center, height_center)
        if number % 10 == 0:
            tick_end = polar_to_cartesian(r - 25, (number * angle + strt_angle), width_center, height_center)
            pygame.draw.line(screen, PINK, tick_start, tick_end, 2)
        elif number % 5 == 0:
            tick_end = polar_to_cartesian(r - 20, (number * angle + strt_angle), width_center, height_center)
            pygame.draw.line(screen, PINK, tick_start, tick_end, 2)
        else:
            tick_end = polar_to_cartesian(r - 15, (number * angle + strt_angle), width_center, height_center)
            pygame.draw.line(screen, PINK, tick_start, tick_end, 2)


def reset_timer(channel):
    global current_time
    current_time = time.time()
