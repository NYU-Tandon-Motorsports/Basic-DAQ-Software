try:
    from gpiozero import CPUTemperature
except Exception as e:
    print("You are not using a Raspberry PI. Please make sure ENABLE_THERMOCOUPLE is False.")

class CPUTemp:
    def __init__(self):
        pass
    def getCPUTEMP(self):
        return CPUTemperature().temperature
