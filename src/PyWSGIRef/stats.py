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

    def export_stats(self, filename: str = None) -> str:
        """
        Exports all current stats as a formatted string.
        If filename is given, it will also save the stats to that file.
        """
        lines = []
        lines.append("PyWSGIRef Statistic-Export")
        lines.append("=" * 30)
        lines.append(f"access counter: {self.count.count}")
        lines.append("")
        lines.append("Performance times:")
        if not self.performanceTimes:
            lines.append("  (no entrys)")
        else:
            for i, perf in enumerate(self.performanceTimes, 1):
                start = getattr(perf, "start", None)
                end = getattr(perf, "end", None)
                title = getattr(perf, "title", "unnamed")
                if start and end:
                    duration = (end - start).total_seconds()
                    lines.append(f"  {i}. {title}: {start} - {end} (duration: {duration:.3f}s)")
                elif start:
                    lines.append(f"  {i}. {title}: started at {start} (not stopped until now)")
                else:
                    lines.append(f"  {i}. {title}: (no time data)")
        result = "\n".join(lines)
        if filename:
            if not filename.endswith(".pywsgirefstats"):
                filename += ".pywsgirefstats"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)
        return result