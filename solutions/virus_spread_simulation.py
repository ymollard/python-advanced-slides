from matplotlib import pyplot
from collections import deque
import numpy as np


class Scenario:
    def __init__(self,
                 incubation_duration: int,
                 duration: int,
                 critical: int,
                 lockdown_duration:int,
                 celebrations: list[int],
                 r0: dict[str, int]):

        self.incubation_duration = incubation_duration
        self.duration = duration
        self.critical = critical
        self.lockdown_duration = lockdown_duration
        self.celebrations = celebrations
        self.r0 = r0
        self.cases_history = [1]
        self.remaining_lockdown_days = 0
        self.r0_history = deque(self.incubation_duration*[1])
        self.lockdowns: list[dict[str, int]] = []

    def next(self, current_date: int, previous_num_cases: int):
        if self.remaining_lockdown_days > 0:
            r0 = self.r0["lockdown"]
            self.remaining_lockdown_days -= 1
        elif self.cases_history[-1] > self.critical and (len(self.lockdowns) == 0 or "end" in self.lockdowns[-1]):
            r0 = self.r0["lockdown"]
            self.lockdowns.append({"start": current_date})
            self.remaining_lockdown_days = self.lockdown_duration
        else:
            if len(self.lockdowns) > 0 and "end" not in self.lockdowns[-1]:
                self.lockdowns[-1].update({"end": current_date})
            r0 = self.r0["regular"]

        if current_date in self.celebrations:
            r0 *= self.r0["high"]

        self.r0_history.append(r0)
        return self.r0_history.popleft()*previous_num_cases

    def plot(self):
        for day in range(self.duration):
            new_cases = self.next(day, self.cases_history[-1])
            self.cases_history.append(new_cases)

        print(self.lockdowns)
        pyplot.plot(range(len(self.cases_history)), self.cases_history, label="Contamination cases")

        # Plot lockdowns green areas
        for lockdown in self.lockdowns:
            pyplot.fill_between([lockdown["start"],
                                 lockdown["end"] if "end" in lockdown else self.duration  # In case the last lockdown
                                                                                          # is not over at the end of the simu
                                 ],
                                0, max(self.cases_history),   # y-values of the colored area
                                color="green", alpha=0.1, label="lockdown")

        # Plot vertical bars for celebrations
        for celebration in self.celebrations:
            pyplot.plot([celebration, celebration], [0, max(self.cases_history)], color="red")

        pyplot.legend()
        pyplot.title("Lockdowns of {} days above {} cases, with {} celebrations and {} days of incubation".format(
                     self.lockdown_duration,
                     self.critical,
                     len(self.celebrations),
                     self.incubation_duration))
        pyplot.xlabel('days')
        pyplot.ylabel('Positive cases')
        pyplot.show()


s = Scenario(
    incubation_duration=15,     # Number of days before the R0 actually changes
    duration=300,               # Days of simulation
    critical=5000,              # Threshold for triggering lockdowns
    lockdown_duration=60,       # Lockdown duration in days
    celebrations=[                    # Individual dates of celebrations:
                    74, 75, 76,       # - These happen during a regular period
                    210, 211, 212     # - These happen during a lockdown period
                 ],
    r0={
        "regular": 1.2,     # R0 value applied for all other cases
        "lockdown": 0.9,  # R0 value applied for lockdowns
        "high": 2  # R0 factor applied for celebrations
    }
)

s.plot()