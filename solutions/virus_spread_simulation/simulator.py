from matplotlib import pyplot
from collections import deque
from logging import getLogger




class Scenario:
    """
    Represents a scenario of virus propagation characterized by simulation parameters
    """
    def __init__(self,
                 incubation_duration: int,
                 duration: int,
                 critical: int,
                 lockdown_duration:int,
                 celebrations: list[int],
                 r0: dict[str, int]):
        """
        Constructor of a scenario
        :param incubation_duration: Number of days before the R0 actually changes
        :param duration: Days of simulation
        :param critical: Threshold for triggering lockdowns
        :param lockdown_duration: Lockdown duration in days
        :param celebrations: Individual dates of celebrations
        :type celebrations: list[int]
        :param r0: Dictionary of R0 values applied for "regular", "lockdown", "high"
        :type r0: dict[str, int]
        """
        self.incubation_duration: int = incubation_duration
        self.duration: int = duration
        self.critical: int = critical
        self.lockdown_duration: int = lockdown_duration
        self.celebrations: list[int] = celebrations
        self.r0: dict[str, int] = r0
        self.cases_history: list[int] = [1]
        self.remaining_lockdown_days: int = 0
        self.r0_history: "deque[int]" = deque(self.incubation_duration*[1])
        self.lockdowns: list[dict[str, int]] = []
        self.logger = getLogger(__name__)

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
            self.logger.debug(f"{self.remaining_lockdown_days} days of lockdown remain")
            r0 = self.r0["lockdown"]
            self.remaining_lockdown_days -= 1
        elif self.cases_history[-1] > self.critical and (len(self.lockdowns) == 0 or "end" in self.lockdowns[-1]):
            self.logger.warning(f"{self.cases_history[-1]} cases reached the critical level ({self.critical}), "
                                f"new lockdown started at {current_date}")
            r0 = self.r0["lockdown"]
            self.lockdowns.append({"start": current_date})
            self.remaining_lockdown_days = self.lockdown_duration
        else:
            if len(self.lockdowns) > 0 and "end" not in self.lockdowns[-1]:
                self.logger.info("Lockdown is over")
                self.lockdowns[-1].update({"end": current_date})
            r0 = self.r0["regular"]

        if current_date in self.celebrations:
            r0 *= self.r0["high"]

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

        # Plot vertical bars for celebrations
        for celebration in self.celebrations:
            pyplot.plot([celebration, celebration], [0, max(self.cases_history)], color="red")

        pyplot.legend()
        pyplot.title(f"Lockdowns of {self.lockdown_duration} days above {self.critical} cases, "
                     f"with {len(self.celebrations)} celebrations and {self.incubation_duration} days of incubation")
        pyplot.xlabel('days')
        pyplot.ylabel('Positive cases')
        pyplot.show()


