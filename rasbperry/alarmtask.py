"""
__author__ = 'Christopher Fagiani'
"""
import datetime

class AlarmTask:
    """Encapsulates a task that will be executed by the alarm engine
    """
    
    def __init__(self, time_string,action):
        self.action = action
        h,m = time_string.split(":")
        self.time = datetime.time(int(h),int(m))
        self.last_run = None

    def execute_if_elapsed(self,now):
        """If the time on this task is at or after the current time AND it's less than curTime+resolution
        """
        if self.time >= datetime.time(now.hour,now.minute) and (self.last_run is None or (now - self.last_run).seconds > ((24*60*60)-1)):
            print "Action triggered at %d:%d" % (now.hour,now.minute)
            self.last_run = now
            self.action()
        
