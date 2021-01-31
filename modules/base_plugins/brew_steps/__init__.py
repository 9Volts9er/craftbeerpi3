# -*- coding: utf-8 -*-
import time


from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi



@cbpi.step
class Rast(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method
    '''
    # Properties
    temp = Property.Number("Temperatur", configurable=True, description="Zieltemperatur des Schritts")
    kettle = StepProperty.Kettle("Kessel", description="Auswahl des Braukessels")
    timer = Property.Number("Timer in Minuten", configurable=True, description="Timer startet, wenn die Zieltemperatur erreicht wurde")

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return:
        '''
        # set target tep
        self.set_target_temp(self.temp, self.kettle)

#    @cbpi.action("Timer manuell starten")
#    def start(self):
#        if self.is_timer_finished() is None:
#            self.start_timer(int(self.timer) * 60)

    def reset(self):
        self.stop_timer()
        self.set_target_temp(self.temp, self.kettle)

    def finish(self):
        pass

    def execute(self):
        '''
        This method is execute in an interval
        :return:
        '''

        # Check if Target Temp is reached
        if self.get_kettle_temp(self.kettle) >= float(self.temp):
            # Check if Timer is Running
            if self.is_timer_finished() is None:
                self.start_timer(int(self.timer) * 60)

        # Check if timer finished and go to next step
        if self.is_timer_finished() == True:
            self.notify("Rast beendet!", "Beginne nächsten Schritt", timeout=None)
            self.next()


@cbpi.step
class Maischen(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method
    '''
    # Properties
    temp = Property.Number("Temperatur", configurable=True,  description="Benachrichtigung bei Erreichen der Ein/Abmaischtemperatur.")
    kettle = StepProperty.Kettle("Kessel", description="Auswahl des Braukessels")
    s = False

    @cbpi.action("Weiter")
    def next_step(self):
        self.set_target_temp(0, self.kettle)
        self.next()

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return:
        '''
        # set target tep
        self.s = False
        self.set_target_temp(self.temp, self.kettle)



    def execute(self):
        '''
        This method is execute in an interval
        :return:
        '''

        # Check if Target Temp is reached
        if self.get_kettle_temp(self.kettle) >= float(self.temp) and self.s is False:
            self.s = True
            self.notify("Maischtemperatur erreicht!", "Bitte maischen und anschließend bestätigen, um fortzufahren.", timeout=None)



@cbpi.step
class Jodprobe(StepBase):

    timer = Property.Number("Timer in Minuten", configurable=True, default_value=0, description="Timer muss manuell gestartet werden")
    notified = False

    @cbpi.action("Verlängern")
    def start(self):
        self.notified = False
        #timer = Property.Number("Timer in Minuten", configurable=True, default_value=0, description="Timer muss manuell gestartet werden")
        if self.is_timer_finished() is None:
            self.start_timer(int(self.timer) * 60)
        else:
            self.stop_timer()
            self.start_timer(int(self.timer) * 60)

    @cbpi.action("Weiter")
    def next_step(self):
        self.next()

    def init(self):
        self.notify("Jodprobe machen", "Verlängern oder nächsten Schritt?", timeout=None)

    def reset(self):
        self.stop_timer()

    def finish(self):
        pass

    def execute(self):
        if self.is_timer_finished() == True and self.notified == False:
            self.notify("Jodprobe machen", "Verlängern oder nächsten Schritt?" , timeout=None)
            self.notified = True

@cbpi.step
class Timer(StepBase):

    timer = Property.Number("Timer in Minuten", configurable=True, default_value=0, description="Timer muss manuell gestartet werden")
    notified = False

    @cbpi.action("Starte Timer")
    def start(self):
        self.notified = False
        #self.timer = Property.Number("Timer in Minuten", configurable=True, default_value=0, description="Timer muss manuell gestartet werden")
        if self.is_timer_finished() is None:
            self.start_timer(int(self.timer) * 60)

    @cbpi.action("Weiter")
    def next_step(self):
        self.next()

    def reset(self):
        self.stop_timer()

    def finish(self):
        pass

    def execute(self):
        if self.is_timer_finished() == True and self.notified == False:
            self.notified = True
            self.notify("Timer abgelaufen", "Verlängern oder nächsten Schritt?" , timeout=None)

#@cbpi.step
#class PumpStep(StepBase):

#    pump = StepProperty.Actor("Pump", description="Pump actor gets toogled")
#    timer = Property.Number("Timer in Minutes", configurable=True, default_value=0, description="Timer is started immediately")

#    @cbpi.action("Stat Timer")
#    def start(self):
#        if self.is_timer_finished() is None:
#            self.start_timer(int(self.timer) * 60)

#    def reset(self):
#        self.stop_timer()


#    def finish(self):
#        self.actor_off(int(self.pump))

#    def init(self):
#        self.actor_on(int(self.pump))

#    def execute(self):
#        if self.is_timer_finished() is None:
#            self.start_timer(int(self.timer) * 60)

#        if self.is_timer_finished() == True:
#            self.next()

@cbpi.step
class Kochen(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method
    '''
    # Properties
#    temp = Property.Number("Temperatur", configurable=True, default_value=100, description="Target temperature for boiling")
    kettle = StepProperty.Kettle("Kessel", description="Auswahl des Braukessels")
    timer = Property.Number("Timer in Minuten", configurable=True, default_value=90, description="Timer muss manuell gestartet werden")
    hop_1 = Property.Number("Hopfengabe 1", configurable=True, description="Erste Hopfengabe nach wie vielen Minuten?")
    hop_1_added = Property.Number("",default_value=None)
    hop_1_exists = True
    hop_2 = Property.Number("Hopfengabe 2", configurable=True, description="Zweite Hopfengabe nach wie vielen Minuten")
    hop_2_added = Property.Number("", default_value=None)
    hop_2_exists = True
    hop_3 = Property.Number("Hopfengabe 3", configurable=True, description="Dritte Hopfengabe nach wie vielen Minuten?")
    hop_3_added = Property.Number("", default_value=None)
    hop_3_exists = True
    hop_4 = Property.Number("Hopfengabe 4", configurable=True, description="Vierte Hopfengabe nach wie vielen Minuten?")
    hop_4_added = Property.Number("", default_value=None)
    hop_4_exists = True
    hop_5 = Property.Number("Hopfengabe 5", configurable=True, description="Fünfte Hopfengabe nach wie vielen Minuten?")
    hop_5_added = Property.Number("", default_value=None)
    hop_5_exists = True

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return:
        '''
        #a = self.get_kettle_auto(self.kettle)
        #self.notify("Auto", "Currently set to: "+str(a), type="info")
        #if a == True:
        #    self.set_kettle_auto(0, self.kettle)
        self.set_target_temp(150, self.kettle)
        self.actor_power(1,100)
        self.actor_on(1,power=None)

        try:
            i = int(self.hop_1)
        except:
            self.hop_1_exists = False
        try:
            i = int(self.hop_2)
        except:
            self.hop_2_exists = False
        try:
            i = int(self.hop_3)
        except:
            self.hop_3_exists = False
        try:
            i = int(self.hop_4)
        except:
            self.hop_4_exists = False
        try:
            i = int(self.hop_5)
        except:
            self.hop_5_exists = False

    @cbpi.action("Starte Koch-Timer")
    def start(self):
        '''
        Custom Action which can be execute form the brewing dashboard.
        All method with decorator @cbpi.action("YOUR CUSTOM NAME") will be available in the user interface
        :return:
        '''
        if self.is_timer_finished() is None:
            self.start_timer(int(self.timer) * 60)

    def reset(self):
        self.stop_timer()
        self.set_target_temp(self.temp, self.kettle)

    def finish(self):
        self.set_target_temp(0, self.kettle)


    def check_hop_timer(self, number, value):
        if self.__getattribute__("hop_%s_added" % number) is not True and time.time() > (self.timer_end - (int(self.timer) * 60 - int(value) * 60)):
            self.__setattr__("hop_%s_added" % number, True)
            self.notify("Hopfengabe", "Hopfengabe %s hinzugeben." % number, timeout=None)

    def execute(self):
        '''
        This method is execute in an interval
        :return:
        '''
        # Check if Timer is Running
        if self.is_timer_finished() is not None:
            if self.hop_1_exists:
                self.check_hop_timer(1, self.hop_1)
            if self.hop_2_exists:
                self.check_hop_timer(2, self.hop_2)
            if self.hop_3_exists:
                self.check_hop_timer(3, self.hop_3)
            if self.hop_4_exists:
                self.check_hop_timer(4, self.hop_4)
            if self.hop_5_exists:
                self.check_hop_timer(5, self.hop_5)
            #self.notify("Running","Running")
            if self.is_timer_finished() == True:
                self.notify("Kochen beendet!", "Starte nächsten Schritt", timeout=None)
                self.next()

@cbpi.step
class Erinnerung(StepBase):

    txt = Property.Text("Erinnerungs-Nachricht", configurable=True, default_value="", description="Erinnerungs-Nachricht wird an dieser Stelle gesendet")

    def init(self):
        self.notify("Erinnerung", txt, timeout=None)
        self.next()
