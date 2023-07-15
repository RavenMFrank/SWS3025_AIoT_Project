import requests
import time
from LightController import LightController
from Sensors.CameraSensor import ImageSensor, VideoSensor
from Sensors.LightSensor import LightSensor
from Sensors.PIRSensor import PIRSensor
from Sensors.TemperatureSensor import TemperatureSensor
from MicrobitCommunication import MicCom

def lightControllerTest():
    pir = PIRSensor()
    lightSensor = LightSensor()
    lightController = LightController(lightSensor, pir)
    lightController.led_on()
    lightController.set_led(1)
    # lightController.adjustTo(0.8)
    print(lightController.lightSensor.get_value())
    input("Press Enter to continue...")

def testMicrobit():
    micro = MicCom()

def PIRtest():
    light = LightController()
    print(light.get_led())
    if light.get_led() == 0:
        light.dark()
def PIRTest():
    pir = PIRSensor()
    light = LightController()
    while True:
        time.sleep(0.1)
        print(pir.get_value())
        if pir.get_value() == 1:
            light.set_led(0.4)
            light.led_on()
            time.sleep(30)
            light.led_off()



if __name__ == '__main__':
    # lightControllerTest()
    # testMicrobit()
    PIRTest()