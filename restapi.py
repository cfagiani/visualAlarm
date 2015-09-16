"""
__author__ = 'Christopher Fagiani'
"""
from flask import Flask, request
import json
import datetime
import threading
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)
apiInstance = None



@app.route("/events", methods=["GET"])
def list_events():
    """lists all events in the system
    """
    global apiInstance
    return apiInstance.list_events()

@app.route("/status", methods=["GET"])
def get_status():
    """returns on/of status of all pins
    """
    global apiInstance
    return apiInstance.get_pin_status()

@app.route("/curtime", methods=["GET"])
def get_curtime():
    """returns the current time on the system
    """
    return '{"curtime":"'+datetime.datetime.now().strftime('%H:%M')+'"}'

@app.route("/events/<name>", methods=["PUT"])
def update_event(name):
    """updates the time for a single event identified by the name passed in via the URL path
    """
    global apiInstance
    return apiInstance.update_event(name,request.args.get('weekdayTime'),request.args.get('weekendTime'))

@app.route("/lights/<name>", methods=["PUT"])
def update_pin(name):
    """
    updates the value of a pin
    :param name: name of pin to update
    """
    global apiInstance
    return '{"status":"'+str(apiInstance.update_light(name, request.args.get('value')))+'"}';

class RestApi:
    def __init__(self,port, alarmDriver):
        """Sets up the Flask webserver to run on the port passed in
        """
        global apiInstance
        self.driver = alarmDriver
        self.port = port
        
        apiInstance = self

    def start(self):
        thread  = threading.Thread(target=self.run_app)
        thread.daemon = False
        thread.start()

    def run_app(self):
        app.run(host="0.0.0.0",port=self.port)

    def get_pin_status(self):
        data = []
        for s in self.driver.get_pin_status():
            data.append(s.to_dict())
        return json.dumps(data)

    def update_light(self,color,value):
        return self.driver.set_light(color, value == 'True')

    def list_events(self):
        """lists all events in the system
        """
        data = []
        for e in self.driver.get_events():
            data.append(e.to_dict())
        return json.dumps(data)

    def update_event(self, name, weekday_time, weekend_time):
        """updates the time for a single event identified by the name passed in via the URL path
        """
        try:
            evt = self.driver.update_event(name,weekday_time,weekend_time)
            if evt is not None:
                return json.dumps(evt.to_dict())
            else:
                return '{"error":"unknown event"}'
        except:
            return '{"error":"invalid time '+time+'"}'
