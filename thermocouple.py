try:
    import board
    import digitalio
    import adafruit_max31855
except Exception as e:
    print("You are not an a raspberry PI. Make sure ENABLE_THERMOCOUPLE is set to FALSE")

class Thermocouple:
    def __init__(self):
        spi = board.SPI()
        cs = digitalio.DigitalInOut(board.D5)
        self.sensor = adafruit_max31855.MAX31855(spi, cs)

    def getTemperature(self):
        return self.sensor.temperature