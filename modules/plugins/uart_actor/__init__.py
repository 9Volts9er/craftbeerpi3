# -*- coding: utf-8 -*-
import time

from modules import cbpi
from modules.core.hardware import ActorBase, SensorPassive, SensorActive
from modules.core.props import Property

import serial

ser = serial.Serial("/dev/serial0",1000000)
#ser.write('s\n')

@cbpi.actor
class UARTSimple(ActorBase):
    maxRPM = Property.Number("Max RPM",configurable=True, description="Maximale Rührgeschwindigkeit")
    stdRPM = Property.Number("Standard RPM",configurable=True,description="Standard Geschwindigkeit")
    power = 10 #stdRPM
    state = 0
    ser = serial.Serial("/dev/serial0",1000000)
    def init(self):
        #start and reset sensor
        pwr = float(self.stdRPM)*100.0/float(self.maxRPM)
        self.set_power(int(pwr))
        try:
            ser.write('s\n')
        except:
            cbpi.notify("Rührwerk Error", "Unable to open serial connection" , type="danger", timeout=None)

    def on(self, power=None):
        rpm = int(self.power)*int(self.maxRPM)/100.0
        try:
            ser.write(str(rpm)+'\n')
            self.state = 1
        except:
            cbpi.notify("Rührwerk Error", "Unable to write to UART", type="danger", timeout=None)

    def set_power(self, power):
        '''
        Optional: Set the power of your actor
        :param power: int value between 0 - maxRPM
        :return:
        '''
        if power is not None:
            self.power = power
            rpm = int(self.power)*int(self.maxRPM)/100.0
            if self.state == 1:
                ser.write(str(rpm)+'\n')

    def off(self):
        rpm = 0
        self.state = 0
        ser.write(str(0)+'\n')




