"""
__author__ = 'Christopher Fagiani'
"""
from flask import Flask, request
import json,sys, datetime, threading

app = Flask(__name__)
apiInstance = None



@app.route("/events", methods=["GET"])
def list_events():
    """lists all events in the system
    """
    global apiInstance
    return apiInstance.list_events()

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
    return apiInstance.update_event(name,request.args.get('time'))

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
        thread.daemon = True
        thread.start()

    def run_app(self):
        app.run(host="0.0.0.0",port=self.port)

    
    def list_events(self):
        """lists all events in the system
        """
        data = []
        for e in self.driver.get_events():
            data.append(e.to_dict())
        return json.dumps(data)

 
    def update_event(self,name,time):
        """updates the time for a single event identified by the name passed in via the URL path
        """
        try:
            evt = self.driver.update_event(name,time)
            if (evt !=None):
                return json.dumps(evt.to_dict())
            else:
                return '{"error":"unkown event"}'  
        except:
            return '{"error":"invalid time '+time+'"}'


       
