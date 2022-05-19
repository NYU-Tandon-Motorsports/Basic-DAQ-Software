try:
    import board
    import digitalio
    import adafruit_lis3dh
    import adafruit_l3gd20
    import busio
except Exception as e:
    print("You are not using a Raspberry PI. Please make sure ENABLE_PI_ACCELEROMETER is False.")

class Accelerometer:
    def __init__(self):
        i2c = board.I2C()
        self.accelerometer = adafruit_lis3dh.LIS3DH_I2C(i2c)
        self.gyro = adafruit_l3gd20.L3GD20_I2C(i2c)
    def getAccel(self):
        x,y,z = self.accelerometer.acceleration
        return(x,y,z)