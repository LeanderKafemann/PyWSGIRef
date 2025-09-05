import datetime

class PerformanceTime:
    def __init__(self, title: str):
        self.start = datetime.datetime.now()
        self.title = title
    def stop(self):
        self.end = datetime.datetime.now()

class RestrictedAccessCounter:
    def __init__(self):
        self._count = 0

    @property
    def count(self) -> int:
        return self._count

    def increase(self):
        self._count += 1

class Stats:
    def __init__(self):
        self.performanceTimes = []
        self.count = RestrictedAccessCounter()

    def startPerfTime(self, title: str = "perfTime") -> PerformanceTime:
        return PerformanceTime(title)
    def stopPerfTime(self, perfTime: PerformanceTime):
        perfTime.stop()
        self.performanceTimes.append(perfTime)