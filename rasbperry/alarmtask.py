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

    def execute_if_elapsed(self,curTime,resolutionTime):
        """If the time on this task is at or after the current time AND it's less than curTime+resolution
            TODO: this doesn't handle the midnight wrap-around
        """
        if self.time >= curTime and self.time< self.addMinutes(curTime,resolutionTime):
            self.action()
        
    def addMinutes(self,tm, mins):
        fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + datetime.timedelta(seconds=mins*60)
        return fulldate.time()
