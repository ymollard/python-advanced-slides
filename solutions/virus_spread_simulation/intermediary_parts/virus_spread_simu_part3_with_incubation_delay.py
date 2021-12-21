from matplotlib import pyplot
from collections import deque


class Scenario:
    """
    Represents a scenario of virus propagation characterized by simulation parameters
    Version with lockdowns and incubation duration but no celebration
    """
    def __init__(self,
                 incubation_duration: int,
                 duration: int,
                 critical: int,
                 lockdown_duration:int,
                 r0: dict[str, int]):
        """
        Constructor of a scenario
        :param incubation_duration: Number of days before the R0 actually changes
        :param duration: Days of simulation
        :param critical: Threshold for triggering lockdowns
        :param lockdown_duration: Lockdown duration in days
        :param r0: Dictionary of R0 values applied for "regular", "lockdown", "high"
        :type r0: dict[str, int]
        """
        self.incubation_duration: int = incubation_duration
        self.duration: int = duration
        self.critical: int = critical
        self.lockdown_duration: int = lockdown_duration
        self.r0: dict[str, int] = r0
        self.cases_history: list[int] = [1]
        self.remaining_lockdown_days: int = 0
        self.r0_history: "deque[int]" = deque(self.incubation_duration*[1])
        self.lockdowns: list[dict[str, int]] = []

    def next(self, current_date: int, previous_num_cases: int):
        """
        Computes the new number of cases for the new day, based on the number of cases from the previous day
        :param current_date: The current date
        :param current_date: int
        :param previous_num_cases: The number of cases from the previous day
        :param previous_num_cases: int
        :return: The new number of cases
        :rtype: int
        """
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

        self.r0_history.append(r0)
        return self.r0_history.popleft()*previous_num_cases

    def plot(self):
        """
        Runs the scenario for every day and display the resulting plot with matplotlib
        """
        for day in range(self.duration):
            new_cases = self.next(day, self.cases_history[-1])
            self.cases_history.append(new_cases)

        pyplot.plot(range(len(self.cases_history)), self.cases_history, label="Contamination cases")

        # Plot lockdowns green areas
        for lockdown in self.lockdowns:
            pyplot.fill_between([lockdown["start"],
                                 lockdown["end"] if "end" in lockdown else self.duration  # In case the last lockdown
                                                                                          # is not over at the end of the simu
                                 ],
                                0, max(self.cases_history),   # y-values of the colored area
                                color="green", alpha=0.1, label="lockdown")

        pyplot.legend()
        pyplot.title(f"Lockdowns of {self.lockdown_duration} days above {self.critical} cases, "
                     f"with {self.incubation_duration} days of incubation but no celebration")
        pyplot.xlabel('days')
        pyplot.ylabel('Positive cases')
        pyplot.show()


if __name__ == "__main__":
    s = Scenario(
        incubation_duration=15,     # Number of days before the R0 actually changes
        duration=300,               # Days of simulation
        critical=5000,              # Threshold for triggering lockdowns
        lockdown_duration=60,       # Lockdown duration in days
        r0={
            "regular": 1.2,     # R0 value applied for all other cases
            "lockdown": 0.9,    # R0 value applied for lockdowns
            "high": 2           # R0 factor applied for celebrations
        }
    )
    s.plot()
