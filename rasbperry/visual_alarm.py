"""
__author__ = 'Christopher Fagiani'
"""
hasGPIO = False
try:
    import RPi.GPIO as GPIO
    hasGPIO = True
except ImportError:
    print "GPIO is not installed. All GPIO operations will be simulated. Please install the module to actually use this utility."

import time, argparse,datetime
from alarmtask import AlarmTask
from threading import Timer

def main(args):
    """This program will use the GPIO capabilities of the raspberry pi to toggle LED lights based on a schedule
    """
    try:
        light1 = int(args.light1)
        light2 = int(args.light2)
        initialize(light1,light2)
        eventList = build_schedule(args.onTime,args.toggleTime,args.offTime,light1,light2)
        run_event_loop(eventList, int(args.resolution))
    finally:
        if hasGPIO:
            GPIO.cleanup()

def run_event_loop(events, intervalMin):
    while True:
        time.sleep(intervalMin*60)
        now = datetime.datetime.now()
        for evt in events:
            evt.execute_if_elapsed(now)

def build_schedule(onTime,offTime,toggleTime,light1,light2):
    events = []
    events.append(AlarmTask(onTime,lambda: set_pin(light1,True)))
    events.append(AlarmTask(toggleTime,lambda: toggle_pins(light1,light2)))
    events.append(AlarmTask(toggleTime,lambda: set_pin(light2,False)))
    return events
    
def toggle_pins(pinToCancel,pinToActivate):
    set_pin(pinToCancel,False)
    set_pin(pinToActivate,True)

def deactivate_pins(pin1,pin2):
    set_pin(pin1,False)
    set_pin(pin2,False)
   
def set_pin(pin,val):
    """Changes the value on the pin passed in
    """
    if hasGPIO:
        GPIO.output(pin,val)
    else:
        print "Set pin %d to %s" % (pin,val)
        
def initialize(light1,light2):
    """Sets upt the GPIO channels and resets them both to OFF
    """
    if hasGPIO:
        GPIO.setmode(GPIO.BCM)
 
        GPIO.setup(light1, GPIO.OUT)
        GPIO.setup(light2,GPIO.OUT)
        deactivate_pins(light1,light2)
    else:
        print("initialized GPIO")
        
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Toggles LED lights based on a schedule")
    #argparser.add_argument("-p","--port", metavar='port',default="8080",help='port for rest api',dest='port')
    argparser.add_argument("-l1","--light1", metavar='lightOne',required=True,help='GPIO pin number for light 1',dest='light1')
    argparser.add_argument("-l2","--light2", metavar='lightTwo',required=True,help='GPIO pin number for light 2',dest='light2')
    argparser.add_argument("-on","--onTime", metavar="onTime",required=True,help="Time (HH:MM UTC) to turn on",dest="onTime")
    argparser.add_argument("-toggle","--toggleTime", metavar="toggleTime",required=True,help="Time (HH:MM UTC) to toggle lights",dest="toggleTime")
    argparser.add_argument("-off","--offTime", metavar="offTime",required=True,help="Time (HH:MM UTC) to turn off",dest="offTime")
    argparser.add_argument("-r","--resolution", metavar='resolution',default=1,help='interval in minutes at which to check for events (mainly used to reduce CPU utilization). If this is more than 1, then it is possible that the lights will not toggle at the exact time specified.',dest='resolution')
    main(argparser.parse_args())
