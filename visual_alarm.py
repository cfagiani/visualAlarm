"""
__author__ = 'Christopher Fagiani'
"""
import time, argparse,datetime
from alarmtask import AlarmTask
from alarm_driver import AlarmDriver
from restapi import RestApi
from threading import Timer


try:
    from flask import Flask
    hasWeb = True
    import restapi
except ImportError:
    print "Flask is not instaled. Please install it to use the RESTful interface"


def main(args):
    """This program will use the GPIO capabilities of the raspberry pi to toggle LED lights based on a schedule
    """
    try:
        driver = AlarmDriver(int(args.light1),int(args.light2))
        driver.build_schedule(args.onTime,args.toggleTime,args.offTime)
        if hasWeb:
            api = RestApi(int(args.port),driver)
            api.start()

        print("Starting event loop")
        driver.run_event_loop(int(args.resolution))
    finally:
        driver.shutdown()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Toggles LED lights based on a schedule")
    argparser.add_argument("-p","--port", metavar='port',default="8080",help='port for rest api',dest='port')
    argparser.add_argument("-l1","--light1", metavar='lightOne',required=True,help='GPIO pin number for light 1',dest='light1')
    argparser.add_argument("-l2","--light2", metavar='lightTwo',required=True,help='GPIO pin number for light 2',dest='light2')
    argparser.add_argument("-on","--onTime", metavar="onTime",required=True,help="Time (HH:MM) to turn on",dest="onTime")
    argparser.add_argument("-toggle","--toggleTime", metavar="toggleTime",required=True,help="Time (HH:MM) to toggle lights",dest="toggleTime")
    argparser.add_argument("-off","--offTime", metavar="offTime",required=True,help="Time (HH:MM) to turn off",dest="offTime")
    argparser.add_argument("-r","--resolution", metavar='resolution',default=1,help='interval in minutes at which to check for events (mainly used to reduce CPU utilization). If this is more than 1, then it is possible that the lights will not toggle at the exact time specified.',dest='resolution')
    main(argparser.parse_args())
