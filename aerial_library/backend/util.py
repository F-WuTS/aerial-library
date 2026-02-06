from typing import Optional

from cflib import crtp
from cflib.crazyflie.log import LogConfig

from aerial_library.api.errors import NoCrazyflieFound


def build_log_config(name: str, period_ms: int, entry_names: set[str]) -> LogConfig:
    if period_ms < 10:
        raise ValueError("period_ms must be at least 10")

    log_config = LogConfig(name=name, period_in_ms=period_ms)

    for entry_name in entry_names:
        log_config.add_variable(entry_name)

    return log_config


def select_connection() -> str:
    available = [uri for uri, _ in crtp.scan_interfaces()]

    match len(available):
        case 0:
            raise NoCrazyflieFound()

        case 1:
            return available[0]

        case _:
            index = _ask_desired_connection(available)
            return available[index]


def _ask_desired_connection(available) -> int:
    print("Multiple connections available:")
    for i, option in enumerate(available):
        print(f"-> {i}: {option}")

    choice: Optional[int] = None
    while choice is None or choice not in range(len(available)):
        try:
            in_str = input("Enter connection number: ")
            choice = int(in_str)

        except ValueError:
            print("Invalid selection, please try again")

    return choice
