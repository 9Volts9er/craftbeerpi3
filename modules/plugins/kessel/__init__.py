from modules import cbpi
from modules.core.controller import KettleController
from modules.core.props import Property


@cbpi.controller
class Kessel(KettleController):

    # Custom Properties

    hyst = Property.Number("Hysterese", True, 0.5, description="The temperature will be hold at target +/- Hysterese.")
    on1600 = Property.Number("1600W Temp", True, 5, description="At which temperature difference 1600W should be activated. Should be smaller than 2500W Temp.")
    on2500 = Property.Number("2500W Temp", True, 10, description="At which temperature difference 2500W should be activated. Should be greater than 1660W Temp.")
    pwr = 0 #heater off
    agitatorID = 2

    def stop(self):
        '''
        Invoked when the automatic is stopped.
        Normally you switch off the actors and clean up everything
        :return: None
        '''
        super(KettleController, self).stop()
        self.pwr = 0
        self.heater_off()


    def run(self):
        '''
        Each controller is exectuted in its own thread. The run method is the entry point
        :return:
        '''
        while self.is_running():

            diff = self.get_target_temp()-self.get_temp()
            if self.pwr == 0:
                if diff > float(self.on2500):
                    self.pwr = 100
                    self.heater_on(100)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)
                elif diff > float(self.on1600):
                    self.pwr = 50
                    self.heater_on(50)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)
                elif diff > float(self.hyst):
                    self.pwr = 20
                    self.heater_on(20)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)

            elif self.pwr > 0 and self.pwr < 36:
                if diff > float(self.on1600)+float(self.hyst):
                    self.pwr = 50
                    self.heater_power(50)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)
                elif diff <= -float(self.hyst):
                    self.pwr = 0
                    self.heater_off()
#                    cbpi.notify("Heating Power","OFF","info",0)
            elif self.pwr >= 36 and self.pwr < 64:
                if diff > float(self.on2500)+float(self.hyst):
                    self.pwr = 100
                    self.heater_power(100)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)
                elif diff <= float(self.on1600)-float(self.hyst):
                    self.pwr = 20
                    self.heater_power(20)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)
            elif self.pwr >= 64:
                if diff <= float(self.on2500) - float(self.hyst):
                    self.pwr = 50
                    self.heater_power(50)
#                    cbpi.notify("Heating Power",str(self.pwr)+"00W","info",0)

            self.sleep(1)
