"""
__author__ = 'Christopher Fagiani'
"""
import time
import datetime
import logging
from alarmtask import AlarmTask

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
except ImportError:
    logger.warn("GPIO not installed")


class AlarmDriver:
    def shutdown(self):
        """Cleans up the GPIO interface
        """
        if self.hasGPIO:
            try:
                self.deactivate_pins()
            except:
                logger.error("Could not deactivate pins prior to shutdown")
            GPIO.cleanup()

    def get_events(self):
        return self.events

    def get_event(self, name):
        """
        returns single event identified by the name
        :param name: name of event
        :return: AlarmTask instance corresponding to the event name or None
        """
        for e in self.events:
            if e.get_name() == name:
                return e
        return None

    def update_event(self, name, weekday_time,weekend_time):
        """
        updates an event with the time passed in
        :param name: name of event to update
        :param weekday_time: string representation of the time (HH:MM format)
        :param weekend_time: string representation of the time (HH:MM format)
        :return:
        """
        evt = self.get_event(name)
        if (evt != None):
            evt.update_time(weekday_time,weekend_time)
            return evt
        return None

    def run_event_loop(self, intervalMin):
        """
        starts an infinite loop that, on each iteration will invoke any events with scheduled times that have
        elapsed. The loop sleeps for intervalMin (set via the resolution command line argument) each iteration.
        :param intervalMin: time, in minutes, the loop will sleep between iterations
        """
        while True:
            time.sleep(intervalMin * 60)
            now = datetime.datetime.now()
            for evt in self.events:
                evt.execute_if_elapsed(now)

    def build_schedule(self, onTime, toggleTime, offTime):
        """
        Forms the list of events
        :param onTime: time for the on event
        :param toggleTime: time for the toggle event
        :param offTime:  time for the off event
        """
        events = []
        events.append(AlarmTask("on", onTime, onTime, lambda: self.toggle_pins(self.pins[1], self.pins[0])))
        events.append(AlarmTask("toggle", toggleTime, toggleTime, lambda: self.toggle_pins(self.pins[0], self.pins[1])))
        events.append(AlarmTask("off", offTime, offTime, lambda: self.deactivate_pins()))
        self.events = events

    def get_pin_status(self):
        """
        :return: an array of Pin objects with updated status (updated by reading the GPIO channels)
        """
        for p in self.pins:
            if self.hasGPIO:
                p.update_status(GPIO.input(p.get_num()))
        return self.pins

    def toggle_pins(self, pinToCancel, pinToActivate):
        """
        turns pinToCancel off and pinToActivate on
        :param pinToCancel: pin to turn off
        :param pinToActivate: pin to turn on
        """
        self.set_pin(pinToCancel, False)
        self.set_pin(pinToActivate, True)

    def deactivate_pins(self):
        """
        turns all pins off
        """
        for p in self.pins:
            self.set_pin(p, False)

    def set_light(self,color,val):
        """
        Sets the pin with the color name that matches the value passed in to the value val
        :param color: color of the light attached to the pin
        :param val: value to set
        :return: True if updated, False if not
        """
        for p in self.pins:
            if p.get_color() == color:
                self.set_pin(p,val)
                return True
        return False

    def set_pin(self, pin, val):
        """
        Changes the value on the pin passed in
        :param pin: pin object to set
        :param val: value to set
        """
        if self.hasGPIO:
            GPIO.output(pin.get_num(), val)
        else:
            if val == 'True':
                pin.update_status(1)
            else:
                pin.update_status(0)
            logger.info("Set pin %d to %s" % (pin.get_num(), val))

    def __init__(self, light1, light2):
        """
        Sets upt the GPIO channels and resets them both to OFF
        :param light1: GPIO channel number for light1
        :param light2: GPIO channel number for light2
        """
        self.hasGPIO = False
        self.events = []
        # do conditional imports (for easiser testing)
        try:
            import RPi.GPIO as GPIO

            self.hasGPIO = True
        except ImportError:
            logger.warn("GPIO is not installed. All GPIO operations will be simulated. Please install the module to actually use this utility.")

        self.pins = []
        self.pins.append(Pin(light1, "red"))
        self.pins.append(Pin(light2, "green"))

        if self.hasGPIO:
            GPIO.setmode(GPIO.BCM)
            for p in self.pins:
                GPIO.setup(p.get_num(), GPIO.OUT, initial=False)

            self.deactivate_pins()
        else:
            logger.info("initialized GPIO")


class Pin:
    def __init__(self, num, color):
        self.num = num
        self.color = color
        self.status = False

    def get_num(self):
        return self.num

    def get_color(self):
        return self.color

    def get_status(self):
        return self.status;

    def update_status(self, val):
        if val == 0:
            self.status = False
        else:
            self.status = True

    def to_dict(self):
        d = {}
        d['pin'] = self.num
        d['color'] = self.color
        d['status'] = self.status
        return d
