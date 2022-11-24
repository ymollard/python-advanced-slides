
from matplotlib import pyplot


class ScenarioIterator:
    """
    Iterator that simulates contamination cases for a certain duration
    """
    def __init__(self, duration, critical, lockdown_duration, r0):
        self.duration: int = duration
        self.r0: dict[str, int] = r0
        self.critical = critical
        self.lockdown_duration = lockdown_duration
        self.remaining_lockdown_days = 0
        self.previous_num_cases = 1
        self.current_date = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.duration is not None and self.current_date > self.duration:
            raise StopIteration()
        
        if self.remaining_lockdown_days > 0:
            r0 = self.r0["lockdown"]
            self.remaining_lockdown_days -= 1
        elif self.previous_num_cases > self.critical and self.remaining_lockdown_days != self.lockdown_duration:
            r0 = self.r0["lockdown"]
            self.remaining_lockdown_days = self.lockdown_duration
        else:
            r0 = self.r0["regular"]

        new_cases = r0*self.previous_num_cases
        self.previous_num_cases = new_cases
        self.current_date += 1

        return new_cases


class Scenario:
    """
    Iterable that can be iterated in a loop
    """
    def __init__(self, duration, critical, lockdown_duration, r0):
        """
        Constructor of a scenario
        :param duration: Numbero of days of simulation
        :param critical: Threshold for triggering lockdowns
        :param lockdown_duration: Lockdown duration in days
        :param r0: Dictionary of R0 values applied for "regular", "lockdown", "high"
        """
        self.duration = duration
        self.r0 = r0
        self.critical = critical
        self.lockdown_duration = lockdown_duration

    def __len__(self):
        return self.duration

    def __iter__(self):
        return ScenarioIterator(self.duration, self.critical, self.lockdown_duration, self.r0)


def plot(iterable):
    cases_history = list(iterable)  # Convert an iterator into a list to force generation until the end
                                    # (make sure there IS an end with StopIterator)
                                    # Note that the conversion make us drop the benefits of the iterator in terms of memory usage
    # pyplot.plot does not accept iterables but only what it assumes looking like a numpy.array, such as a list
    pyplot.plot(range(len(cases_history)), cases_history, label="Contamination cases")

    pyplot.legend()
    pyplot.xlabel('days')
    pyplot.ylabel('Positive cases')
    pyplot.show()


if __name__ == "__main__":
    scenario = Scenario(
        duration=300,               # Days of simulation
        critical=5000,              # Threshold for triggering lockdowns
        lockdown_duration=60,       # Lockdown duration in days
        r0={
            "lockdown": 0.9,    # R0 applied for lockdowns
            "regular": 1.2,     # R0 applied for all other cases
        }
    )
    plot(scenario)
