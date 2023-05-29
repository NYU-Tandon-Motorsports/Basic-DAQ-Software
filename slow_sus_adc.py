try:
    import board
    import digitalio
    import adafruit_ads1x15.ads1015 as ADS
    from adafruit_ads1x15.ads1x15 import Mode
    from adafruit_ads1x15.analog_in import AnalogIn
    import busio
except Exception as e:
    print("You are not using a Raspberry PI. Please make sure ENABLE_PI_ACCELEROMETER is False.")

class SlowSusADC:
    def __init__(self):
        i2c = board.I2C()
        self.sus_adc = ADS.ADS1015(i2c, address=0x4A)
        self.testchan = AnalogIn(self.sus_adc, ADS.P0)
        self.testchan2 = AnalogIn(self.sus_adc, ADS.P1)
    def getVals(self):
        vals = (self.testchan.value, self.testchan2.value)
        return(vals)