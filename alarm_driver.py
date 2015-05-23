"""
__author__ = 'Christopher Fagiani'
"""
import time, argparse,datetime, threading
from alarmtask import AlarmTask
from threading import Timer

class AlarmDriver:

    def shutdown(self):
        """Cleans up the GPIO interface
        """
        if self.hasGPIO:
            GPIO.cleanup()

    def get_events(self):
        return self.events

    def get_event(self,name):
        for e in self.events:
            if e.get_name() == name:
                return e
        return None

    def update_event(self,name,time):
        evt = self.get_event(name)
        if (evt != None):
            evt.update_time(time)
            return evt
        return None
        
    def run_event_loop(self, intervalMin):
        """starts an infinite loop that, on each iteration will invoke any events with scheduled times that have elapsed. The loop sleeps for intervalMin (set via the resolution command line argument) each iteration.
        """
        while True:
            time.sleep(intervalMin*60)
            now = datetime.datetime.now()
            for evt in self.events:
                evt.execute_if_elapsed(now)

    def build_schedule(self,onTime,toggleTime,offTime):
        """Forms the list of events
        """
        events = []
        events.append(AlarmTask("on",onTime,lambda: self.set_pin(self.light1,True)))
        events.append(AlarmTask("toggle",toggleTime,lambda: self.toggle_pins(self.light1,self.light2)))
        events.append(AlarmTask("off",offTime,lambda: self.set_pin(self.light2,False)))
        self.events=events
        
    def toggle_pins(self,pinToCancel,pinToActivate):
        """turns pinToCancel off and pinToActivate on
        """
        self.set_pin(pinToCancel,False)
        self.set_pin(pinToActivate,True)

    def deactivate_pins(self, pin1,pin2):
        """turns both pins off
        """
        self.set_pin(pin1,False)
        self.set_pin(pin2,False)
       
    def set_pin(self,pin,val):
        """Changes the value on the pin passed in
        """
        if self.hasGPIO:
            GPIO.output(pin,val)
        else:
            print "Set pin %d to %s" % (pin,val)
            
    def __init__(self, light1,light2):
        """Sets upt the GPIO channels and resets them both to OFF
        """
        self.hasGPIO = False
        self.events = []
        #do conditional imports (for easiser testing)
        try:
            import RPi.GPIO as GPIO
            self.hasGPIO = True
        except ImportError:
            print "GPIO is not installed. All GPIO operations will be simulated. Please install the module to actually use this utility."

        self.light1 = light1
        self.light2 = light2
        if self.hasGPIO:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(light1, GPIO.OUT)
            GPIO.setup(light2,GPIO.OUT)
            deactivate_pins(light1,light2)
        else:
            print("initialized GPIO")
            
