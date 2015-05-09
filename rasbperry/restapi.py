"""
__author__ = 'Christopher Fagiani'
"""
from flask import Flask
import json,sys

app = Flask(__name__)
    
events = []

def initialize(port, event_list):
    global events
    events= event_list
    app.run(port=port)


@app.route("/events")
def list_events():
    global events
    data = []
    for e in events:  
        data.append(e.to_dict())
    return json.dumps(data)
