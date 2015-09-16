"""
__author__ = 'Christopher Fagiani'
"""
import datetime
import logging

logger = logging.getLogger(__name__)


class AlarmTask:
    """Encapsulates a task that will be executed by the alarm engine
    """

    def __init__(self, name, weekday_time_string, weekend_time_string, action, one_time=False):
        """
        Constructor. Sets the target even time to the value represented by time_string (format should be HH:MM).
        :param name: name of the event
        :param time_string: string representation (in HH:MM format) of time event should fire
        :param action: function that will be called
        :param one_time: flag indicating this is a one-time event
        :return: initialized object
        """
        self.name = name
        self.action = action
        self.one_time = one_time

        h, m = weekday_time_string.split(":")
        self.weekday_time = datetime.time(int(h), int(m))

        h, m = weekend_time_string.split(":")
        self.weekend_time = datetime.time(int(h), int(m))

        self.last_run = None

    def execute_if_elapsed(self, now):
        """
        If the time on this task is at or after the current time AND it's been more than 24 hours since last run
        :param now: current time
        """
        target_time = self.weekday_time
        if (now.weekday() >= 5):
            target_time = self.weekend_time
        if target_time <= datetime.time(now.hour, now.minute) and self.__shouldExecute(now, target_time):
            logger.info("Action %s triggered at %02d:%02d. Scheduled for %02d:%02d" % (
                self.name, now.hour, now.minute, target_time.hour, target_time.minute))
            self.last_run = now
            self.action()

    def __shouldExecute(self, now, event_time):
        """
        Checks now against the last_run for this event and returns a flag indicating if the event should fire.
         Events should fire iff it's
        :param now: current time
        :return: True if the task should fire, False if not
        """
        if self.last_run is None:
            window = now - datetime.timedelta(minutes=30)
            if event_time >= datetime.time(window.hour, window.minute):
                return True
            else:
                logger.debug("Not firing %s since we're out of the execution window" % self.name)
                return False
        elif (now - self.last_run).total_seconds() >= (24 * 60 * 59):
            return True

    def to_dict(self):
        """
        returns a dictionary representation of the fields of this object
        :return: dictionary containing the data fields of this object
        """
        d = {}
        d['name'] = self.name
        d['weekday-time'] = self.weekday_time.strftime('%H:%M')
        d['weekend-time'] = self.weekend_time.strftime('%H:%M')
        d['last'] = str(self.last_run)
        d['onetime'] = self.one_time
        return d

    def get_name(self):
        """
        :return: name of event
        """
        return self.name

    def update_time(self, weekday_time_string, weekend_time_string):
        """
        updates the time property to the value passed in AND resets the last_run property to None
        :param time_string: string to which the time will be set
        """
        h, m = weekday_time_string.split(":")
        self.weekday_time = datetime.time(int(h), int(m))
        h, m = weekend_time_string.split(":")
        self.weekend_time = datetime.time(int(h), int(m))
        self.last_run = None
