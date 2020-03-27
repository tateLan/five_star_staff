import config
import datetime
import threading
import time
from queue import Queue
import sys


class TimeTracker(threading.Thread):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.logger = model.logger
        self.notifier = model.notifier
        self.upcoming_shifts = Queue()

    def run(self):
        try:
            while True:
                self.get_upcoming_shifts()
                if self.upcoming_shifts.queue.__len__() > 0:
                    time_left_to_shift = self.get_time_left_to_shift()

                    for notification in time_left_to_shift:
                        menu_id = self.model.get_staff_main_menu_msg_id(notification[0])
                        self.notifier.notify_waiter_about_upcoming_shift(notification, menu_id)
                time.sleep(config.TIME_TRACKER_SECONDS_PERIOD)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'time tracker')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'time tracker')

    def get_upcoming_shifts(self):
        """
        Filling queue with upcoming shifts, staff registered on
        :return: None
        """
        try:
            shifts = self.model.get_upcoming_shifts_for_notifier()

            for shift in shifts:
                self.upcoming_shifts.put(shift)
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'time tracker')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'time tracker')

    def get_time_left_to_shift(self):
        """
        Calculates how much time left to shift, and adds shift registration to list,
            if staff needs to be informed (if left 24 hours, 3 hours)
        :return: list with sets of shift registrations, staff needs to be informed (staff_id,
                                                                                    time left,
                                                                                    date starts,
                                                                                    event title)
        """
        try:
            date = datetime.datetime.now()
            res = []

            day_start_line = datetime.timedelta(0, 86100)
            day_end_line = datetime.timedelta(1, 300)

            three_hour_start_line = datetime.timedelta(0, 10500)
            three_hour_end_line = datetime.timedelta(0, 11100)

            for sh_reg in self.upcoming_shifts.queue:
                diff = sh_reg[3] - date
                if day_start_line <= diff <= day_end_line:
                    res.append((sh_reg[0], '24 години', sh_reg[3], sh_reg[4]))
                elif three_hour_start_line <= diff <= three_hour_end_line:
                    res.append((sh_reg[0], '3 години', sh_reg[3], sh_reg[4]))

            return res
        except Exception as err:
            method_name = sys._getframe().f_code.co_name

            self.logger.write_to_log('exception', 'time tracker')
            self.logger.write_to_err_log(f'exception in method {method_name} - {err}', 'time tracker')

