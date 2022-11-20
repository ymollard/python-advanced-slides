from matplotlib import pyplot


class ScenarioIterator:
    """
    Iterator that simulates contamination cases for a certain duration
    """
    def __init__(self, duration, r0):
        self.duration = duration
        self.r0 = r0
        self.previous_num_cases = 1
        self.current_date = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.duration is not None and self.current_date > self.duration:
            raise StopIteration()
        
        r0 = self.r0["regular"]
        new_cases = r0*self.previous_num_cases
        self.previous_num_cases = new_cases
        self.current_date += 1

        return new_cases


class Scenario:
    """
    Iterable that can be iterated in a loop
    """
    def __init__(self, duration, r0):
        """
        Constructor of a scenario
        :param duration: Number of days of simulation
        :param r0: Dictionary of R0 values applied for "regular", "lockdown", "high"
        """
        self.duration = duration
        self.r0 = r0

    def __iter__(self):
        return ScenarioIterator(self.duration, self.r0)


def plot(iterable):
    cases_history = list(iterable)  # Convert an iterator into a list to force generation until the end
                                    # (make sure there IS an end with StopIterator)
                                    # Note that the conversion make us drop the benefits of the iterator in terms of memory usage
    pyplot.plot(range(len(cases_history)), cases_history, label="Contamination cases")

    pyplot.legend()
    pyplot.xlabel('days')
    pyplot.ylabel('Positive cases')
    pyplot.show()


if __name__ == "__main__":
    scenario_iter = Scenario(
        duration=300,               # Days of simulation
        r0={
            "regular": 1.2,     # R0 value applied for all other cases
        }
    )

    plot(scenario_iter)
