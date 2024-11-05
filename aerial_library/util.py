from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig


def build_log_config(name: str, period_ms: int, entry_names: [str, ...]) -> LogConfig:
    if period_ms < 10:
        raise ValueError('period_ms must be at least 10')

    log_config = LogConfig(name=name, period_in_ms=period_ms)

    for entry_name in entry_names:
        log_config.add_variable(entry_name)

    return log_config


def has_flow_deck(crazyflie: Crazyflie) -> bool:
    value_str = crazyflie.param.get_value('deck.bcFlow2', 5)
    return bool(int(value_str))
