from logging import getLogger, StreamHandler
from simulator import Scenario

log = getLogger("simulator")
handler = StreamHandler()
handler.setLevel("DEBUG")
log.addHandler(handler)
log.setLevel("DEBUG")

if __name__ == "__main__":
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
            "lockdown": 0.9,    # R0 value applied for lockdowns
            "high": 2           # R0 factor applied for celebrations
        }
    )

    s.plot()
