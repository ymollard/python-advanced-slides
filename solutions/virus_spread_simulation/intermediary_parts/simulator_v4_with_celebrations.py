
from matplotlib import pyplot


class ScenarioIterator:
    """
    Iterator that simulates contamination cases for a certain duration
    """
    def __init__(self, duration, critical, lockdown_duration, celebrations, r0):
        self.duration = duration
        self.r0 = r0
        self.critical = critical
        self.lockdown_duration = lockdown_duration
        self.remaining_lockdown_days = 0
        self.previous_num_cases = 1
        self.current_date = 0
        self.celebrations = celebrations

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

        if self.current_date in self.celebrations:
            r0 *= self.r0["high"]

        new_cases = r0 * self.previous_num_cases
        self.previous_num_cases = new_cases
        self.current_date += 1

        return new_cases


class Scenario:
    """
    Iterable that can be iterated in a loop
    """
    def __init__(self, duration, critical, lockdown_duration, celebrations, r0):
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
        self.celebrations = celebrations
        self.iter = ScenarioIterator(self.duration, self.critical, self.lockdown_duration, self.celebrations, self.r0)

    def __len__(self):
        return self.duration

    def __iter__(self):
        return self.iter

    def __getitem__(self, item):
        output = []
        for i in range(item.start, item.stop):
            try:
                output.append(next(self.iter))
            except StopIteration:
                pass
        return output


def plot(iterable):
    start = 0  # The lower boundary of the window of 300 days is day #0
    while True:
        stop = start + 300
        cases_history = iterable[start:stop]

        if len(cases_history) == 0:
            return

        # Plot vertical bars for celebrations
        for celebration in iterable.celebrations:
            if start < celebration < stop:
                pyplot.plot([celebration, celebration], [0, max(cases_history)], color="red")

        # pyplot.plot does not accept iterables but only what it assumes looking like a numpy.array, such as a list
        pyplot.plot(range(start, start + len(cases_history)), cases_history, label="Contamination cases")

        pyplot.legend()
        pyplot.xlabel('days')
        pyplot.ylabel('Positive cases')
        pyplot.show()

        start = stop


if __name__ == "__main__":
    scenario = Scenario(
        duration=950,               # Days of simulation
        critical=5000,              # Threshold for triggering lockdowns
        lockdown_duration=60,       # Lockdown duration in days
        celebrations=[
            74, 75, 76,  # Individual dates of celebrations
            210, 211, 450, 680,
            710, 920
        ],
        r0={
            "high": 2,          # R0 applied for celebrations
            "lockdown": 0.9,    # R0 applied for lockdowns
            "regular": 1.2,     # R0 applied for all other cases
        }
    )
    plot(scenario)
