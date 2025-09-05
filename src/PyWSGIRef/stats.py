import datetime

class PerformanceTime:
    def __init__(self, title: str):
        self.start = datetime.datetime.now()
        self.title = title
    def stop(self):
        self.end = datetime.datetime.now()

class Stats:
    def __init__(self):
        self.performanceTimes = []

    def startPerfTime(self, title: str = "perfTime") -> PerformanceTime:
        return PerformanceTime(title)
    def stopPerfTime(self, perfTime: PerformanceTime):
        perfTime.stop()
        self.performanceTimes.append(perfTime)