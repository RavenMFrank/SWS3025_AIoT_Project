import time
from gpiozero import PWMLED
from Sensors.LightSensor import LightSensor
from Sensors.PIRSensor import PIRSensor
import numpy as np


def sigmoid(x) -> float:
    return 1 / (1 + np.exp(-x))


def invSigmoid(x) -> float:
    return np.log(x / (1 - x))


class LightController:
    def __init__(self, lightSensor: LightSensor = LightSensor("lightSensor"),
                 pirSensor: PIRSensor = PIRSensor("PIRSensor"), adjustFunc=sigmoid,
                 invAdjustFunc=invSigmoid, adjustDuration=0.5, adjustTotalSteps=15):
        self.led = PWMLED(21)
        self.lightSensor = lightSensor
        self.PIRSensor = pirSensor
        self.adjustFunc = adjustFunc
        self.invAdjustFunc = invAdjustFunc
        self.adjustDuration = adjustDuration
        self.adjustTotalSteps = adjustTotalSteps

    def led_off(self):
        self.led.off()

    def led_on(self):
        self.led.on()

    def get_led(self):
        # return the value of led in [0,1]
        return self.led.value

    def set_led(self, value):
        self.led.value = value

    def set_state(self, mode):
        if mode == 'manual':  # 手动模式
            self.led.value = 0.8  # 默认亮度
            self.led.on()
        elif mode == 'reading':  # 阅读模式
            self.led.value = 0.8  # 默认亮度
            self.led.on()
            targetBrightness = 0.009
            i = 0
            while (i < 100):
                self.adjustTo(targetBrightness)
                i = i + 1
        elif mode == 'computer':  # 电脑模式
            self.led.value = 0.8  # 默认亮度
            self.led.on()
            targetBrightness = 0.02
            i = 0
            while (i < 100):
                self.adjustTo(targetBrightness)
                i = i + 1

    def adjustTo(self, targetBrightness):
        currentBrightness = self.get_led()
        startX = self.invAdjustFunc(currentBrightness)
        endX = self.invAdjustFunc(targetBrightness)
        step = (endX - startX) / self.adjustTotalSteps
        for i in range(self.adjustTotalSteps):
            self.set_led(self.adjustFunc(startX + step * i))
            time.sleep(self.adjustDuration / self.adjustTotalSteps)
        # lightIntensity = self.lightSensor.get_value()
        # if lightIntensity > ideaLight + 0.001:  # 暗
        #     if self.led.value + 0.001 < 1:
        #         self.led.value = self.led.value + 0.001
        #     else:
        #         self.led.value = 1
        # elif lightIntensity < ideaLight - 0.001:  # 亮
        #     if self.led.value - 0.001 > 0:
        #         self.led.value = self.led.value - 0.001
        # else:
        #     self.led.value = 0

    def dark(self):
        while True:
            if self.PIRSensor.get_value() == 1 and self.get_led() == 0:
                print(self.get_led())
                self.led_on()
                print(self.get_led())
                time.sleep(10)
                self.led_off()
