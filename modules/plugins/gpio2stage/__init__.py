# -*- coding: utf-8 -*-
import time

from modules import cbpi
from modules.core.hardware import ActorBase, SensorPassive, SensorActive
from modules.core.props import Property

try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except Exception as e:
    print e
    pass



@cbpi.actor
class GPIO2PIN(ActorBase):

    gpio900 = Property.Select("GPIO 900W", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], description="GPIO to which the 900W heater is connected")
    gpio1600 = Property.Select("GPIO 1600W", options=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27], description="GPIO to which the 1600W heater is connected")

    power = 9  # *100 watt, options: 9,16,25

    def init(self):
        GPIO.setup(int(self.gpio900), GPIO.OUT)
        GPIO.output(int(self.gpio900), 0)
        GPIO.setup(int(self.gpio1600), GPIO.OUT)
        GPIO.output(int(self.gpio1600), 0)

#    def get_unit(self):
#        return "00W"

    def on(self, power=None):
        if power is not None:
            self.power = int(power)

        if self.power > 0:
            GPIO.output(int(self.gpio900), 1)
            GPIO.output(int(self.gpio1600), 0)
        if self.power >= 36:
            GPIO.output(int(self.gpio1600), 1)
            GPIO.output(int(self.gpio900), 0)
        if self.power >= 64:
            GPIO.output(int(self.gpio900), 1)
            GPIO.output(int(self.gpio1600), 1)

    def set_power(self, power):
        '''
        Optional: Set the power of your actor
        :param power: int value between 0 - 100
        :return: 
        '''
        if power is not None:
            self.power = int(power)

        if self.power > 0:
            GPIO.output(int(self.gpio900), 1)
            GPIO.output(int(self.gpio1600), 0)
        if self.power >= 36:
            GPIO.output(int(self.gpio1600), 1)
            GPIO.output(int(self.gpio900), 0)
        if self.power >= 64:
            GPIO.output(int(self.gpio900), 1)
            GPIO.output(int(self.gpio1600), 1)

    def off(self):
        GPIO.output(int(self.gpio900), 0)
        GPIO.output(int(self.gpio1600), 0)


