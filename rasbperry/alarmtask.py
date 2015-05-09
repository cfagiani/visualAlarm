"""
__author__ = 'Christopher Fagiani'
"""
import datetime

class AlarmTask:
    """Encapsulates a task that will be executed by the alarm engine
    """
    
    def __init__(self, time_string,action):
        """constructor. Sets the target even titme to the value represented by time_string (format should be HH:MM). 
        """
        self.action = action
        h,m = time_string.split(":")
        self.time = datetime.time(int(h),int(m))
        self.last_run = None

    def execute_if_elapsed(self,now):
        """If the time on this task is at or after the current time AND it's been more than 24 hours since last run
        """
        if self.time <= datetime.time(now.hour,now.minute) and (self.last_run is None or (now - self.last_run).seconds > (24*60*60)):
            #print "Action triggered at %02d:%02d. Scheduled for %02d:%02d" % (now.hour,now.minute, self.time.hour,self.time.minute)
            self.last_run = now
            self.action()
        
