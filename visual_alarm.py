"""
__author__ = 'Christopher Fagiani'
"""
import argparse
import logging
import sys
from alarm_driver import AlarmDriver



try:
    from flask import Flask
    hasWeb = True
except ImportError:
    print "Flask is not installed. Please install it to use the RESTful interface"


def main(args):
    """This program will use the GPIO capabilities of the raspberry pi to toggle LED lights based on a schedule
    """
    driver = None
    try:

        logger = logging.getLogger(__name__)
        driver = AlarmDriver(int(args.light1),int(args.light2))
        driver.build_schedule(args.onTime,args.toggleTime,args.offTime)
        if hasWeb:
            from restapi import RestApi
            api = RestApi(int(args.port),driver)
            api.start()
        logger.info("Starting event loop")
        driver.run_event_loop(int(args.resolution))
    finally:
        if driver is not None:
            driver.shutdown()

def configure_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

if __name__ == "__main__":
    configure_logger()
    argparser = argparse.ArgumentParser(description="Toggles LED lights based on a schedule")
    argparser.add_argument("-p","--port", metavar='port',default="8080",help='port for rest api',dest='port')
    argparser.add_argument("-l1","--light1", metavar='lightOne',required=True,help='GPIO pin number for light 1',dest='light1')
    argparser.add_argument("-l2","--light2", metavar='lightTwo',required=True,help='GPIO pin number for light 2',dest='light2')
    argparser.add_argument("-on","--onTime", metavar="onTime",required=True,help="Time (HH:MM) to turn on",dest="onTime")
    argparser.add_argument("-toggle","--toggleTime", metavar="toggleTime",required=True,help="Time (HH:MM) to toggle lights",dest="toggleTime")
    argparser.add_argument("-off","--offTime", metavar="offTime",required=True,help="Time (HH:MM) to turn off",dest="offTime")
    argparser.add_argument("-r","--resolution", metavar='resolution',default=1,help='interval in minutes at which to check for events (mainly used to reduce CPU utilization). If this is more than 1, then it is possible that the lights will not toggle at the exact time specified.',dest='resolution')
    main(argparser.parse_args())
