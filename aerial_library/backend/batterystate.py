from enum import Enum


class BatteryState(Enum):
    Discharging = 0
    Charging = 1
    DoneCharging = 2
    Low = 3
    Shutdown = 4  # TODO figure out meaning
