import os
import time
import traceback
import keyboard
import serial
from serial.tools import list_ports
from datetime import datetime
import driver_telemetry
from mercury_telemetry_pipeline import Pipeline
import datapoint
from formulas import Formulas
import sensor_ids
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from thermocouple import Thermocouple
from picputemp import CPUTemp
from piaccelerometer import Accelerometer
from pigyro import Gyro
from fast_sus_ADC import SusADC
from datapoint import Datapoint
import GPS
import RPi.GPIO as GPIO

SERIAL_ARDUINO_COUNT = 1  # hard coded value for now will determine how many arduinos there are
ENABLE_PIACCELEROMETER = False
ENABLE_THERMOCOUPLE = True
ENABLE_PI_CPUTEMP = False
ENABLE_GPS = False
ENABLE_ADC = False
ENABLE_GYRO = False

MERCURY_TIMEOUT = 0.5  #Wait time between post requests sent to live telemetry

def collect_data(serial_in, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    mercury_last_sent = 0
    while(True):  # Condition for when to stop the program currently 60 seconds

        output, mercury_last_sent = parse_serial(serial_in, formula_calc, mercury_telemetry_pipeline, mercury_last_sent)
        if output != "" and output is not None and ord(output[0]) != 0:
            log.write(bytes(output, 'utf-8').decode('utf-8', 'ignore') + "\n")
    serial_in.close()

def collect_temperatures(thermocouple, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    mercury_last_sent = 0
    while (True):  # Condition for when to stop the program currently 60 seconds
        output = ""
        try:
            temperature = thermocouple.getTemperature()
            data_capture_time = time.time()
            data = Datapoint(sensor_ids.ELECTRONICS_THERMOCOUPLE, "CVT Temperature", 1, ["temperature"], [temperature], ["C"], data_capture_time - start_time)
            formula_calc.apply_calculation(data)
            output = str(data)
            driver_telemetry.send_data(data)
            if data_capture_time - mercury_last_sent > MERCURY_TIMEOUT:
                mercury_telemetry_pipeline.send_packet(data)
                mercury_last_sent = data_capture_time
        except Exception as e:
            output = str(traceback.format_exc())
        print(output)
        try:
            print(GPIO.input(21))
        except Exception as e:
            traceback.print_exc()
        log.write(output + "\n")
        time.sleep(1)

def collect_CPUTemps(cputemp, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    mercury_last_sent = 0
    while (True):  # Condition for when to stop the program currently 60 seconds
        output = ""
        try:
            temperature = cputemp.getCPUTEMP()
            data_capture_time = time.time()
            data = Datapoint(sensor_ids.CPUTEMP, "CPU Temperature", 1, ["temperature"], [temperature], ["C"], data_capture_time - start_time)
            formula_calc.apply_calculation(data)
            output = str(data)
            driver_telemetry.send_data(data)
            if data_capture_time - mercury_last_sent > MERCURY_TIMEOUT:
                mercury_telemetry_pipeline.send_packet(data)
                mercury_last_sent = data_capture_time
        except Exception as e:
            output = str(traceback.format_exc())
        print(output)
        log.write(output + "\n")
        time.sleep(1)



def collect_accelerations(accelerometer, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    mercury_last_sent = 0
    while (True):  # Condition for when to stop the program currently 60 seconds
        output = ""
        try:
            acceleration = accelerometer.getAccel()
            data_capture_time = time.time()
            data = Datapoint(sensor_ids.PIACCELEROMETER, "Accelerometer", 3, ["x","y","z"], acceleration, ["m/s2","m/s2","m/s2"], data_capture_time - start_time)
            formula_calc.apply_calculation(data)
            output = str(data)
            driver_telemetry.send_data(data)
            if data_capture_time - mercury_last_sent > MERCURY_TIMEOUT:
                mercury_telemetry_pipeline.send_packet(data)
                mercury_last_sent = data_capture_time
        except Exception as e:
            output = str(traceback.format_exc())
        print(output)
        log.write(output + "\n")
        time.sleep(0.1)

def collect_gyro(gyro, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    mercury_last_sent = 0
    while (True):  # Condition for when to stop the program currently 60 seconds
        output = ""
        try:
            acceleration = gyro.getAccel()
            data_capture_time = time.time()
            data = Datapoint(sensor_ids.PIGYRO, "Gyro", 3, ["yaw","pitch","roll"], acceleration, ["m/s2","m/s2","m/s2"], data_capture_time - start_time)
            formula_calc.apply_calculation(data)
            output = str(data)
            driver_telemetry.send_data(data)
            if data_capture_time - mercury_last_sent > MERCURY_TIMEOUT:
                mercury_telemetry_pipeline.send_packet(data)
                mercury_last_sent = data_capture_time
        except Exception as e:
            output = str(traceback.format_exc())
        print(output)
        log.write(output + "\n")
        time.sleep(0.1)

def collect_sus_angles(adc, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    mercury_last_sent = 0
    while (True):  # Condition for when to stop the program currently 60 seconds
        output = ""
        try:
            angle = adc.getVals()
            data_capture_time = time.time()
            data = Datapoint(sensor_ids.SUS_ADC, "Sus-Angles", 3, ["FL","FR","RL", "RR"], [0,angle,0,0], ["deg","deg","deg","deg"], data_capture_time - start_time)
            formula_calc.apply_calculation(data)
            output = str(data)
            driver_telemetry.send_data(data)
            if data_capture_time - mercury_last_sent > MERCURY_TIMEOUT:
                mercury_telemetry_pipeline.send_packet(data)
                mercury_last_sent = data_capture_time
        except Exception as e:
            output = str(traceback.format_exc())
        print(output)
        log.write(output + "\n")
        time.sleep(0.001)

def collect_gps(gps_port, formula_calc, mercury_telemetry_pipeline, log):
    start_time = time.time()
    while (True):  # Condition for when to stop the program currently 60 seconds
        output = ""
        raw = gps_port.readline().decode('utf-8')
        result = GPS.parseGPS(raw)
        if result is not None: #if result is none then we ignore and read the next serial line
            if result == (-1,-1,-1,-1, -1, -1):
                output = "ERROR: GPS has invalid fix. Please wait for it to recalibrate and make sure you are outside and your antenna is good"
                mercury_telemetry_pipeline.send_log("No GPS Fix")
            else:
                datapoints = datapoint.get_gps_datapoints(result)
                for dp in datapoints:
                    formula_calc.apply_calculation(dp)
                    output += "\n" + str(dp)
                    driver_telemetry.send_data(dp)
                    mercury_telemetry_pipeline.send_packet(dp)
            print(output)
            log.write(output + "\n")
        time.sleep(0.1)



def parse_serial(serial_in, formula_calc, mercury_telemetry_pipeline, mercury_last_sent):
    raw = serial_in.readline()
    data_capture_time = time.time()
    output = ""
    try:  # the try block is here because the serial stream can sometimes have extraneous bytes that cant be converted to plain text such as 00, 0A, etc.
        output = raw.decode()  # decode the binary stream
        output = output.strip()  # removing extra spaces and LFs from serial stream
        if output[0:3] == "///":  # Checking for three character signature in the beginning of each serial line to tell the parser what the purpose of the input is
            output = ""  # nothing is printed
        elif output[0:3] == "###":
            output = "INFO: " + output[3:]  # info
            print(output)
            mercury_telemetry_pipeline.send_log(output)
        elif output[0:3] == "!!!":
            output = "ERROR: " + output[3:]  # error
            print(output)
            mercury_telemetry_pipeline.send_log(output)
        elif output[0:3] == "$$$":
            error = False
            data = None
            try:
                data = datapoint.get_datapoint_from_arduino_raw(output)
            except Exception as e:
                print(e)
                error = True
            if (error == False):
                formula_calc.apply_calculation(data)
                output = str(data)
                print(output)
                driver_telemetry.send_data(data)
                if data_capture_time - mercury_last_sent > MERCURY_TIMEOUT:
                    mercury_telemetry_pipeline.send_packet(data)
                    mercury_last_sent = data_capture_time
        else:
            print(output)  # unmarked serial input
    except UnicodeDecodeError:  # serial decode didnt work
        output = ""
    return output, mercury_last_sent

def main():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.add_event_detect(21, GPIO.BOTH, callback=reset_timer)

    finally:
        GPIO.cleanup()


    now = datetime.now()
    mercury_telemetry_pipeline = Pipeline()
    log = open(os.getcwd()+"/datalogs/serialdata_" + now.strftime("%m%d%Y_%H-%M-%S") + ".txt", "x")  # timestamping the text file and making a new log
    ## serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    log.write("Serial data obtained from USB connection on " + now.strftime("%m/%d/%Y %H:%M:%S")+"\n\n")
    gps_device_signature = '2c7c:0125'
    arduino_device_signature = "1a86:7523"#'0403:6015'#'0403:6015'#10c4:ea60'#
    gps_candidates = list(list_ports.grep(gps_device_signature))
    gps_candidates.reverse()
    arduino_candidates = list(list_ports.grep(arduino_device_signature))
    arduino_candidates.reverse()
    log.write("DAQ: Initializing " + str(len(arduino_candidates)) + " Arduino(s)\n")
    print("DAQ: Initializing " + str(len(arduino_candidates)) + " Arduino(s)")
    mercury_telemetry_pipeline.send_log("DAQ: Initializing " + str(len(arduino_candidates)) + " Arduino(s)")
    serial_inputs = [serial.Serial(arduino_candidate.device, 9600, timeout=1) for arduino_candidate in arduino_candidates]  # creates SERIAL_ARDUINO_COUNT serial inputs
    log.write("DAQ: Successfully Initialized " + str(len(arduino_candidates)) + " Arduino(s)\n")
    print("DAQ: Successfully Initialized " + str(len(arduino_candidates)) + " Arduino(s)")
    mercury_telemetry_pipeline.send_log("DAQ: Successfully Initialized " + str(len(arduino_candidates)) + " Arduino(s)")
    """Each serial in represents an arduino plugged in VIA USB. Each arduino requires a separate serial instance"""
    # serial_in2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    thermocouple = None
    cputemp = None
    accelerometer = None
    gyro = None
    adc = None
    if (ENABLE_THERMOCOUPLE):
        log.write("DAQ: Testing Thermocouple\n")
        print("DAQ: Testing Thermocouple")
        mercury_telemetry_pipeline.send_log("DAQ: Testing Thermocouple")
        thermocouple = Thermocouple()
        test = thermocouple.getTemperature()
        log.write("DAQ: Thermocouple test Successful\n")
        print("DAQ: Thermocouple test Successful")
    if (ENABLE_PI_CPUTEMP):
        log.write("DAQ: Testing CPU Temp\n")
        print("DAQ: Testing CPU Temp")
        mercury_telemetry_pipeline.send_log("DAQ: Testing CPU Temp")
        cputemp = CPUTemp()
        test = cputemp.getCPUTEMP()
        log.write("DAQ: CPU Temp test Successful\n")
        print("DAQ: CPU Temp test Successful")
    if (ENABLE_PIACCELEROMETER):
        log.write("DAQ: Testing Accelerometer\n")
        print("DAQ: Testing Accelerometer")
        mercury_telemetry_pipeline.send_log("DAQ: Testing Accelerometer")
        accelerometer = Accelerometer()
        test = accelerometer.getAccel()
        log.write("DAQ: Accelerometer test Successful\n")
        print("DAQ: Accelerometer test Successful")
        mercury_telemetry_pipeline.send_log("DAQ: Accelerometer test Successful")
    if (ENABLE_GYRO):
        log.write("DAQ: Testing Gyro\n")
        print("DAQ: Testing Gyro")
        mercury_telemetry_pipeline.send_log("DAQ: Testing Gyro")
        gyro = Gyro()
        test = gyro.getAccel()
        log.write("DAQ: Gyro test Successful\n")
        print("DAQ: Gyro test Successful")
        mercury_telemetry_pipeline.send_log("DAQ: Gyro test Successful")
    if (ENABLE_ADC):
        log.write("DAQ: Testing ADC\n")
        print("DAQ: Testing ADC")
        mercury_telemetry_pipeline.send_log("DAQ: Testing ADC")
        adc = SusADC()
        test = adc.getVals()
        log.write("DAQ: ADC test Successful\n")
        print("DAQ: ADC test Successful")
        mercury_telemetry_pipeline.send_log("DAQ: ADC test Successful")
    if (ENABLE_GPS):
        print("DAQ: Testing GPS make sure the port is NOT busy")
        log.write("DAQ: Testing GPS make sure the port is NOT busy\n")
        mercury_telemetry_pipeline.send_log("DAQ: Testing GPS make sure the port is NOT busy")
        GPS.set_candidates(gps_candidates)
        GPS.testGPS()
        log.write("DAQ: GPS test Successful\n")
        print("DAQ: GPS test Successful")
        mercury_telemetry_pipeline.send_log("DAQ: GPS test Successful")
    formula_calc= Formulas()
    log.write("Initializing Formulas\n")
    print("Initializing Formulas")
    mercury_telemetry_pipeline.send_log("Initializing Formulas")

    driver_telemetry.init_driver_telem()

    executor = ThreadPoolExecutor(max_workers=len(arduino_candidates) + ENABLE_THERMOCOUPLE + ENABLE_PI_CPUTEMP + ENABLE_PIACCELEROMETER +ENABLE_GYRO+ENABLE_GPS + ENABLE_ADC)
    futures = []
    print("starting sensor read threads (press shift+q to quit)")
    for serial_in in serial_inputs:
        args = [serial_in, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_data, *args))

    if (ENABLE_THERMOCOUPLE):
        args = [thermocouple, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_temperatures, *args))
    if (ENABLE_PI_CPUTEMP):
        args = [cputemp, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_CPUTemps, *args))
    if (ENABLE_PIACCELEROMETER):
        args = [accelerometer, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_accelerations, *args))
    if (ENABLE_GYRO):
        args = [gyro, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_gyro, *args))
    if (ENABLE_ADC):
        args = [adc, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_sus_angles, *args))
    if ENABLE_GPS:
        gps_ser = serial.Serial(GPS.port, baudrate=115200, timeout=0.5, rtscts=True, dsrdtr=True)
        args = [gps_ser, formula_calc, mercury_telemetry_pipeline, log]
        futures.append(executor.submit(collect_gps, *args))

    concurrent.futures.wait(futures)
    time.sleep(2)
    print("DAQ Program exiting with code 0")
    log.write("DAQ Program exiting with code 0\n")
    mercury_telemetry_pipeline.send_log("DAQ Program exiting with code 0")
    log.close()
    exit()

main()
