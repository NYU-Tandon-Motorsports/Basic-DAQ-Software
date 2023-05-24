try:
    import board
    import digitalio
    import adafruit_pct2075
    import busio
except Exception as e:
    print("You are not using a Raspberry PI. Please make sure ENABLE_THERMOCOUPLE is False.")


class Thermocouple:
    def __init__(self):
        i2c = board.I2C()
        self.pct = adafruit_pct2075.PCT2075(i2c)


    def getTemperature(self):
        return self.pct.temperature