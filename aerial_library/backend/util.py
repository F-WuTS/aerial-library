from cflib import crtp
from cflib.crazyflie.log import LogConfig

from aerial_library.api.errors import CrazyflieNotFound, InvalidCrazyflieAddress


def build_log_config(name: str, period_ms: int, entry_names: set[str]) -> LogConfig:
    if period_ms < 10:
        raise ValueError("period_ms must be at least 10")

    log_config = LogConfig(name=name, period_in_ms=period_ms)

    for entry_name in entry_names:
        log_config.add_variable(entry_name)

    return log_config


def select_connection(address: str) -> str:
    numerical_address = _parse_crazyflie_address(address)

    available = [uri for uri, _ in crtp.scan_interfaces(numerical_address)]

    if len(available) == 0:
        raise CrazyflieNotFound(address)

    index = _ask_desired_connection(available)
    return available[index]


def _parse_crazyflie_address(address: str) -> int:
    invalid_address_error = InvalidCrazyflieAddress(address)

    if len(address) != 10:
        raise invalid_address_error

    if not all(digit in "0123456789abcdefABCDEF" for digit in address):
        raise invalid_address_error

    try:
        return int(address, 16)
    except ValueError as e:
        raise invalid_address_error from e


def _ask_desired_connection(available) -> int:
    print("Available connections:")
    for i, option in enumerate(available):
        print(f"-> {i}: {option}")

    while True:
        in_str = input("Enter connection number: ")


        if not in_str.isdigit():
            print("Invalid input, please try again")
            continue

        choice = int(in_str)

        if choice not in range(len(available)):
            print("Invalid selection, please try again")
            continue

        return choice

    raise RuntimeError("Unreachable")
