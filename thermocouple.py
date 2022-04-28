try:
    import board
    import digitalio
    import adafruit_max31855
    import busio
except Exception as e:
    print("You are not using a Raspberry PI. Please make sure ENABLE_THERMOCOUPLE is False.")


class Thermocouple:
    def __init__(self):
        spi = busio.SPI(board.D11, MOSI = None, MISO = board.D9)
        cs = digitalio.DigitalInOut(board.D5)
        self.sensor = adafruit_max31855.MAX31855(spi, cs)

    def getTemperature(self):
        return self.sensor.temperature