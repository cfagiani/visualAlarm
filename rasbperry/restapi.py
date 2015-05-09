"""
__author__ = 'Christopher Fagiani'
"""
from flask import Flask
from flask import request
import json,sys

app = Flask(__name__)
    
events = []

def initialize(port, event_list):
    global events
    events= event_list
    app.run(port=port)


@app.route("/events", methods=["GET"])
def list_events():
    """lists all events in the system
    """
    global events
    data = []
    for e in events:  
        data.append(e.to_dict())
    return json.dumps(data)

@app.route("/events/<name>", methods=["PUT"])
def update_event(name):
    global events
    for e in events:
        if e.get_name() == name:
            if(e.update_time(request.args.get('time'))):
                return json.dumps(e.to_dict())
            else:
                return "{'error':'invalid time "+request.args.get('time')+"'}"
    return "{'error':'unkown event'}"

