import time

class TimeMeasurement:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        
        
    def start(self):
        if self.start_time is not None:
            raise Exception("Timer is running. Use .end() to stop it")
        self.start_time = time.time()
        
        
    def end(self):
        if self.start_time is None:
            raise Exception("Timer is not running. Use .start() to start it")
        self.end_time = time.time()
        
    @property
    def duration(self):
        if self.end_time is None:
            raise Exception("Timer has not been stopped yet")
        if self.start_time is None:
            raise Exception("Timer has not been started yet")
        return self.end_time - self.start_time