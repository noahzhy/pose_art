import datetime
import time


class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.timer_started = False

    def start(self):
        self.start_time = datetime.datetime.now()
        self.timer_started = True

    def stop(self):
        self.timer_started = False

    def get_time(self):
        self.end_time = datetime.datetime.now()
        # second, e.g. 1.004187
        return (self.end_time-self.start_time).total_seconds()

    def timer_started(self):
        return self.timer_started


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    time.sleep(1)
    end_time = datetime.datetime.now()
    print((end_time-start_time).total_seconds())