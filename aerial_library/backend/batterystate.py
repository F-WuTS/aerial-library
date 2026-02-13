from enum import Enum


class BatteryState(Enum):
    Discharging = 0
    Charging = 1
    DoneCharging = 2
    Low = 3
    Shutdown = 4  # TODO figure out meaning

    def __str__(self) -> str:
        name_map = {
            BatteryState.Discharging: "discharging",
            BatteryState.Charging: "charging",
            BatteryState.DoneCharging: "done charging",
            BatteryState.Low: "low",
            BatteryState.Shutdown: "shutdown",
        }

        return name_map[self]
