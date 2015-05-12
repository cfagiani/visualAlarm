"""
__author__ = 'Christopher Fagiani'
"""
from flask import Flask
from flask import request
import json,sys, datetime

app = Flask(__name__)
    
events = []

def initialize(port, event_list):
    """Sets up the Flask webserver to run on the port passed in
    """
    global events
    events= event_list
    app.run(host="0.0.0.0",port=port)


@app.route("/events", methods=["GET"])
def list_events():
    """lists all events in the system
    """
    global events
    data = []
    for e in events:  
        data.append(e.to_dict())
    return json.dumps(data)

@app.route("/curtime", methods=["GET"])
def get_curtime():
    """returns the current time on the system
    """
    return '{"curtime":"'+datetime.datetime.now().strftime('%H:%M')+'"}'

@app.route("/events/<name>", methods=["PUT"])
def update_event(name):
    """updates the time for a single event identified by the name passed in via the URL path
    """
    global events
    for e in events:
        if e.get_name() == name:
            if(e.update_time(request.args.get('time'))):
                return json.dumps(e.to_dict())
            else:
                return '{"error":"invalid time '+request.args.get('time')+'"}'
    return '{"error":"unkown event"}'

