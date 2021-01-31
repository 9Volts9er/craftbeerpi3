from modules import cbpi
from modules.core.hardware import  SensorActive
from modules.core.props import Property

import serial

ser = serial.Serial("/dev/serial0",1000000,timeout=0.5)

@cbpi.sensor
class RPMSensor(SensorActive):

    interval = Property.Number("Update Interval", configurable=True, default_value=1)
    #interval = 0.1
    rpm = 0

    @cbpi.action("Reset Sensor")
    def reset_sensor(self):
        ser.write('s\n')
        line = ser.read_until('\n')
        if "ok" in line:
            cbpi.notify("Sensor Reset","Sensor reset successfull!","info",timeout=None)
        else:
            cbpi.notify("Sensor Reset","Sensor reset failed!","danger",timeout=None)
            cbpi.notify("Sensor says", str(line), "info", timeout=None)
        pass

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''
        return "RPM"

    def stop(self):
        '''
        Stop the sensor. Is called when the sensor config is updated or the sensor is deleted
        :return: 
        '''
        pass

    def execute(self):
        '''
        Active sensor has to handle its own loop
        :return: 
        '''
        while self.is_running():
            ser.reset_input_buffer()
            ser.write('g\n')
            line = ser.read_until('\n')
            self.rpm = float(line)
            self.data_received(self.rpm)
            self.sleep(float(self.interval))

    @classmethod
    def init_global(cls):
        '''
        Called one at the startup for all sensors
        :return: 
        '''
